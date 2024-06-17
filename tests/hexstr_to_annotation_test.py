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


def test_comma_0xhex_long():
    data = """
    0x3a, 0x01, 0x05, 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x5f, 0x70, 0x69, 0x63, 0x6b, 0x75, 0x70
    """
    info: HexInfo = hex_str_to_annotation(data, protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == '3a 01 05 62 72 69 64 67 65 5f 70 69 63 6b 75 70'

def test_comma_0xhex_trailing_comma():
    data = """
    0x3a, 0x01, 0x05, 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x5f, 0x70, 0x69, 0x63, 0x6b, 0x75, 0x70,
    """
    info: HexInfo = hex_str_to_annotation(data, protocol_6=True, protocol_7=True)
    print(info)
    assert info['bytes'] == '3a 01 05 62 72 69 64 67 65 5f 70 69 63 6b 75 70'

def test_comma_0xhex_multiline():
    # real 0.7 only packet payload
    data = """
		0x3a, 0x01, 0x05, 0x62, 0x72, 0x69, 0x64, 0x67, 0x65, 0x5f, 0x70, 0x69, 0x63, 0x6b, 0x75, 0x70, 0x73,
		0x00, 0x91, 0xa7, 0xf2, 0xa0, 0x05, 0x8b, 0x11, 0x08, 0xa8, 0x15, 0xa9, 0x19, 0x38, 0xaf, 0xfd, 0xb6,
		0xcb, 0xf1, 0xdb, 0x5a, 0xfc, 0x73, 0x34, 0xae, 0xa3, 0x68, 0xa7, 0xfa, 0x35, 0x54, 0x37, 0xf9, 0x39,
		0x96, 0xd6, 0x05, 0x25, 0xef, 0x7b, 0x22, 0x40, 0x9d,
    """
    info: HexInfo = hex_str_to_annotation(data, protocol_6=False, protocol_7=True)
    print(info)
    assert info['bytes'] == (
        '3a 01 05 62 72 69 64 67 65 5f 70 69 63 6b 75 70 73 00 91 a7 f2 a0 05 8b 11 08 '
        'a8 15 a9 19 38 af fd b6 cb f1 db 5a fc 73 34 ae a3 68 a7 fa 35 54 37 f9 39 96 '
        'd6 05 25 ef 7b 22 40 9d'
    )

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

