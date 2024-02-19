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
    # ethernet
    try:
        ip = dpkt.ethernet.Ethernet(data).data
        if not isinstance(ip.data, dpkt.udp.UDP):
            print("ethernet but not udp payload")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ethernet packet ...")
    except:
        pass
    # ipv6
    try:
        ip = dpkt.ip6.IP6(data)
        print(ip.data)
        if not isinstance(ip.data, dpkt.udp.UDP):
            print("ipv6 but not udp payload")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ipv6 packet ...")
    except:
        pass
    # ipv4
    try:
        ip = dpkt.ip.IP(data)
        print(ip.data)
        if not isinstance(ip.data, dpkt.udp.UDP):
            print("ipv4 but not udp payload")
            raise ValueError("not udp")
        udp_payload = ip.data.data
        messages.append("extracting udp payload from ipv4 packet ...")
    except:
        pass

    data = udp_payload
    return (data, messages)
