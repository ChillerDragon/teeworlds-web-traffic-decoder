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
            print("not ethernet")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ethernet packet ...")
    except:
        pass
    try:
        ip = dpkt.ip.IP(data)
        print(ip.data)
        if not isinstance(ip.data, dpkt.udp.UDP):
            print("not udp")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ip packet ...")
    except:
        pass

    data = udp_payload
    return (data, messages)



# data = \
#     b'\x60\x0a\xa5\x6d\x00\x1d\x11\x40\x00\x00\x00\x00\x00\x00\x00\x00' \
#     b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00' \
#     b'\x00\x00\x00\x00\x00\x00\x00\x01\x20\x6f\xd9\xc8\x00\x1d\x00\x30' \
#     b'\x00\x19\x02\x23\xec\x92\x03\x00\x05\x15\x9e\xa0\x05\x0c\x00\x05' \
#     b'\x0f\x9e\xa0\x05\x02'
# 
# print(extract_udp_payload(data))
