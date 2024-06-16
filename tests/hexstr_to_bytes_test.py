from src.tw_packet_decoder import str_to_bytes

def test_basic_hex():
    assert str_to_bytes('ff') == b'\xff'
    assert str_to_bytes('ffaa') == b'\xff\xaa'
    assert str_to_bytes('ff aa') == b'\xff\xaa'
    assert str_to_bytes('ff            aa') == b'\xff\xaa'

def test_0xhex():
    assert str_to_bytes('0xff') == b'\xff'
    assert str_to_bytes('0xFF') == b'\xff'
    assert str_to_bytes('0xff 0xaa') == b'\xff\xaa'
    assert str_to_bytes('0xff0xaa') == b'\xff\xaa'
    assert str_to_bytes('          0xff   \n\n\t         0xaa') == b'\xff\xaa'

def test_0xhex_comma():
    assert str_to_bytes('0xff, 0xaa') == b'\xff\xaa'
    assert str_to_bytes('0xff,0xaa') == b'\xff\xaa'
    assert str_to_bytes('0xff ,0xaa') == b'\xff\xaa'
    assert str_to_bytes('0xff ,0xaa\n\n,\n   0xdd') == b'\xff\xaa\xdd'

def test_0xhex_invalid_comma():
    assert str_to_bytes('0xff ,0xaa 0xdd') == b'\xff\xaa\xdd'

