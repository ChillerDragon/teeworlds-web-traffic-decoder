import re

# lines = ["03:11:31.128677 IP6 localhost.55752 > localhost.8303: UDP, length 8",
# "        0x0000:  6004 33b1 0010 1140 0000 0000 0000 0000  `.3....@........",
# "        0x0010:  0000 0000 0000 0001 0000 0000 0000 0000  ................",
# "        0x0020:  0000 0000 0000 0001 d9c8 206f 0010 0023  ...........o...#",
# "        0x0030:  040f 0026 3e5a 3704                      ...&>Z7."]
#
# hex_from_tcpdump(lines) == ['6004 33b1 0010 1140', '0000 0000 0000 0001', '0000 0000 0000 0001', '040f 0026 3e5a 3704']

def hex_from_tcpdump(lines):
    hex_lines = []
    for line in lines:
        m = re.match(r'^\s*0x\d{4}:\s+(([0-9a-fA-F]{4}\s+){3}([0-9a-fA-F]{4}))', line)
        if m:
            hex_lines.append(m[1])
    return hex_lines
