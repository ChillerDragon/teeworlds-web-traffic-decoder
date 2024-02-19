import dpkt
from typing import Tuple, List

def extract_udp_payload(data: bytes) -> Tuple[bytes, List[str]]:
    """
    turns bytes into just the bytes that are the udp payload
    if it detects bytes to be an ethernet or ip udp package
    otherwise it just returns the raw bytes

    if it did find a udp payload it will say so in the
    array of strings contained in the return value
    """
    messages: List[str] = []
    udp_payload = data
    try:
        ip = dpkt.ethernet.Ethernet(data).data
        if not isinstance(ip.data, dpkt.udp.UDP):
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ethernet packet ...")
    except (ValueError, AttributeError):
        pass
    try:
        ip = dpkt.ip.IP(data)
        print(ip.data)
        if not isinstance(ip.data, dpkt.udp.UDP):
            print("not udp")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ip packet ...")
    except ValueError:
        pass

    data = udp_payload
    return (data, messages)


# data = \
#     b'\x60\x04\x33\xb1\x00\x10\x11\x40\x00\x00\x00\x00\x00\x00\x00\x00' \
#     b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00' \
#     b'\x00\x00\x00\x00\x00\x00\x00\x01\xd9\xc8\x20\x6f\x00\x10\x00\x23' \
#     b'\x04\x0f\x00\x26\x3e\x5a\x37\x04'
# 
# print(extract_udp_payload(data))


data = \
    b'\x45\x00\x00\x35\x1a\xeb\x40\x00\x40\x11\x21\xcb\x7f\x00\x00\x01' \
    b'\x7f\x00\x00\x01\xf3\x67\x20\x6f\x00\x21\xfe\x34\x10\x0c\x01\x42' \
    b'\x78\x0d\x88\x55\xe9\xf0\x87\xe6\x07\x68\xd6\xd0\x5b\xf8\x69\x2f' \
    b'\xff\x8c\x14\x37\x00'

got = extract_udp_payload(data)
expect = (b'\x10\x0c\x01Bx\r\x88U\xe9\xf0\x87\xe6\x07h\xd6\xd0[\xf8i/\xff\x8c\x147\x00', ['extracting udp payload from ip packet ...'])
print(got == expect)

