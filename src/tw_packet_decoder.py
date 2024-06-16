import traceback

import re
import ast
from importlib.metadata import version
from typing import TypedDict

import twnet_parser.packet
import twnet_parser.huffman
from twnet_parser.packet import TwPacket

from .tcpdump import hex_from_tcpdump
from .udp import extract_udp_payload

def str_to_bytes(data: str) -> bytes:
    data = data.strip()
    if re.match('^b[\'\"].*[\'\"]$', data):
        return ast.literal_eval(data)

    if re.match('^0x', data):
        data = data.replace('0x', '')

    return bytes(bytearray.fromhex(data))

def twpacket_to_str(packet: TwPacket) -> str:
    messages = []
    messages.append(str(packet.header))
    for msg in packet.messages:
        messages.append(str(msg))
    return '\n'.join(messages).replace('<', '&lt;').replace('>', '&gt;')

class HexInfo(TypedDict):
    message: str
    bytes: str

def hex_str_to_annotation(hex_str: str, protocol_6: bool, protocol_7: bool) -> HexInfo:
    # data = """  4500 0035 1aeb 4000 4011 21cb 7f00 0001
    #   7f00 0001 f367 206f 0021 fe34 100c 0142
    #     780d 8855 e9f0 87e6 0768 d6d0 5bf8 692f
    #       ff8c 1437 00
    #       """
    # print(str_to_bytes(data).hex(sep = " ")) == "45 00 00 35 1a eb 40 00 40 11 21 cb 7f 00 00 01 7f 00 00 01 f3 67 20 6f 00 21 fe 34 10 0c 01 42 78 0d 88 55 e9 f0 87 e6 07 68 d6 d0 5b f8 69 2f ff 8c 14 37 00"
    # data = r"b'\x04\x00\x011\xe4\xc3\xd6\x00\x19\x030.7 802f1be60a05665f\x00\x00\x85\x1c'"
    # print(str_to_bytes(data))
    # data = "02 7e 01 48 1f 93 d7 40 10 0a 80 01 6f 70 74 69 6f 6e 00 74 65 73 74 00 00 00"
    # print(str_to_bytes(data))
    # data = "0x02 0xff 0x03"
    # print(str_to_bytes(data))

    invalid_hex = False

    try:
        data = str_to_bytes(hex_str)
    except ValueError:
        invalid_hex = True

    if invalid_hex:
        hex_str = hex_from_tcpdump(hex_str.split('\n'))
        if len(hex_str) == 0:
            return { 'message': 'invalid hex', 'bytes': '' }
        try:
            data = str_to_bytes(' '.join(hex_str))
        except ValueError:
            return { 'message': 'invalid hex', 'bytes': '' }

    data, messages = extract_udp_payload(data)

    messages.append(f"[twnet_parser v{version('twnet_parser')}][huffman={twnet_parser.huffman.backend_name()}] udp payload: {data.hex(sep = ' ')}")

    if protocol_7:
        messages.append("--- 0.7")
        try:
            packet = twnet_parser.packet.parse7(data)
            messages.append(twpacket_to_str(packet))
        except Exception:
            messages.append(traceback.format_exc())

    if protocol_6:
        messages.append("--- 0.6")
        try:
            packet = twnet_parser.packet.parse6(data)
            messages.append(twpacket_to_str(packet))
        except Exception:
            messages.append(traceback.format_exc())

    if not protocol_6 and not protocol_7:
        messages.append('No protocol selected. Not decoding.')

    return { 'message': '\n'.join(messages), 'bytes': data.hex(sep = ' ') }
