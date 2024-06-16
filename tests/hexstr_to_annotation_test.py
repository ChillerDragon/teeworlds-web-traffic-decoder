from src.tw_packet_decoder import HexInfo, hex_str_to_annotation

def test_basic_hex():
    info: HexInfo = hex_str_to_annotation('ff', protocol_6=True, protocol_7=True)
    assert info['bytes'] == 'ff'

def test_grouped_hex_udp_payload():
    data = """  4500 0035 1aeb 4000 4011 21cb 7f00 0001
      7f00 0001 f367 206f 0021 fe34 100c 0142
        780d 8855 e9f0 87e6 0768 d6d0 5bf8 692f
          ff8c 1437 00
    """
    # also extracts udp payload
    info: HexInfo = hex_str_to_annotation(data, protocol_6=True, protocol_7=True)
    assert info['bytes'] == '10 0c 01 42 78 0d 88 55 e9 f0 87 e6 07 68 d6 d0 5b f8 69 2f ff 8c 14 37 00'

def test_py_bytestr_double_quote():
    info: HexInfo = hex_str_to_annotation(r'b"\xff"', protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == 'ff'

def test_py_bytestr_single_quote():
    info: HexInfo = hex_str_to_annotation(r"b'\xff\xaa'", protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == 'ff aa'

def test_spaced_0xhex():
    info: HexInfo = hex_str_to_annotation('0x00 0x01 0xff', protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == '00 01 ff'

def test_comma_0xhex():
    info: HexInfo = hex_str_to_annotation('0x00,0x01,0xff', protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == '00 01 ff'

def test_space_comma_0xhex():
    info: HexInfo = hex_str_to_annotation('0x01, 0x02', protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == '01 02'

def test_tpcudmp_payload_misleading_pairs():
    data = """
        03:11:31.128677 IP6 localhost.55752 > localhost.8303: UDP, length 8"
                0x0000:  6004 33b1 0010 1140 0000 0000 0000 0000 1111 `.3....@........
                0x0010:  0000 0000 0000 0001 0000 0000 0000 0000 2222 3333  ................
                0x0020:  0000 0000 0000 0001 d9c8 206f 0010 0023  ...........o...#
                0x0030:  040f 0026 3e5a 3704                      ...&>Z7.
    """
    info: HexInfo = hex_str_to_annotation(data, protocol_6=True, protocol_7=True)
    assert info['bytes'] == '04 0f 00 26 3e 5a 37 04'


def test_tpcudmp_payload_misleading_pairs_and_ascii_dump():
    data = r"""
        03:11:31.128677 IP6 localhost.55752 > localhost.8303: UDP, length 8"
                0x0000:  6004 33b1 0010 1140 0000 0000 0000 0000 1111 `.3....@........ b"\xff"
                0x0010:  0000 0000 0000 0001 0000 0000 0000 0000 2222 3333  ........b''.......
                0x0020:  0000 0000 0000 0001 d9c8 206f 0010 0023  ...........o...# []byte { 0xff, 0xaa }
                0x0030:  040f 0026 3e5a 3704                      ...&>Z7. [0xaa, 0xdd]
    """
    info: HexInfo = hex_str_to_annotation(data, protocol_6=True, protocol_7=True)
    assert info['bytes'] == '04 0f 00 26 3e 5a 37 04'

