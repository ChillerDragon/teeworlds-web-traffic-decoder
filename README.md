# teeworlds-web-traffic-decoder
Paste your raw teeworlds traffic as hex and get annotations about which package that is

![image](https://github.com/ChillerDragon/teeworlds-web-traffic-decoder/assets/20344300/2fe66dc9-564a-4e54-b94d-a0cdc56b187e)


### setup

    python -m pip install -r requirements.txt

### run development server

    FLASK_ENV=development FLASK_APP=main.py flask run

Then goto http://localhost:5000/ in your browser

## api usage

```
$ curl -s http://127.0.0.1:5000/api/v1/decode/ff -X POST | jq .message -r
[twnet_parser v0.8.0][huffman=rust-libtw2] udp payload: ff
--- 0.7
Traceback (most recent call last):
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/main.py", line 89, in hex_str_to_annotation
    packet = twnet_parser.packet.parse7(data)
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/venv/lib/python3.10/site-packages/twnet_parser/packet.py", line 472, in parse7
    return PacketParser().parse7(data, we_are_a_client)
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/venv/lib/python3.10/site-packages/twnet_parser/packet.py", line 453, in parse7
    ctrl_msg: CtrlMessage = match_control7(data[header_size], data[8:], client)
IndexError: index out of range

--- 0.6
Traceback (most recent call last):
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/main.py", line 96, in hex_str_to_annotation
    packet = twnet_parser.packet.parse6(data)
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/venv/lib/python3.10/site-packages/twnet_parser/packet.py", line 469, in parse6
    return PacketParser().parse6(data, we_are_a_client)
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/venv/lib/python3.10/site-packages/twnet_parser/packet.py", line 428, in parse6
    connless_msg: ConnlessMessage = match_connless6(data[header_size:14], data[14:])
  File "/home/chiller/Desktop/git/teeworlds-web-traffic-decoder/venv/lib/python3.10/site-packages/twnet_parser/msg_matcher/connless6.py", line 58, in match_connless6
    f"Error: unknown conless  message id={msg_id!r} data={data[0]}"
IndexError: index out of range

```

## development

run tests

```
pytest .
```

