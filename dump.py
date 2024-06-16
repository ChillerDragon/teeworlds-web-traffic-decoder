#!/usr/bin/env python3

import twnet_parser.packet
packet = twnet_parser.packet.parse7(bytes.fromhex("000101010203043a01056272696467655f7069636b7570730091a7f2a0058b1108a815a91938affdb6cbf1db5afc7334aea368a7fa355437f93996d60525ef7b22409d"))         
print(str(packet.header))

header = packet.header

header_dict = {}
header_dict["flags"] = []
if header.flags.resend:
    header_dict["flags"].append("resend")
if header.flags.connless:
    header_dict["flags"].append("connless")
if header.flags.compression:
    header_dict["flags"].append("compression")
if header.flags.control:
    header_dict["flags"].append("control")
header_dict["ack"] = header.ack
header_dict["token"] = header.token
header_dict["num_chunks"] = header.num_chunks
header_dict["connless_version"] = header.connless_version
header_dict["response_token"] = header.response_token

print("")

print(header_dict)

# <class: 'PacketHeader'>: {'flags': <class: 'PacketFlags7'>, 'ack': 1, 'token': b'\x01\x02\x03\x04', 'num_chunks': 1, 'connless_version': 1, 'response_token': b'\xff\xff\xff\xff'}                                 
