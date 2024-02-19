#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request

import src.log_config
import src.tw_packet_decoder

app = Flask(__name__)

def req_ipaddr() -> str:
    print(request)
    if not 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.remote_addr
    return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()

@app.route('/')
def index():
    return render_template('index.html.j2', foo = "bar")

@app.route('/api/v1/decode/<string:packet>', methods=["POST"])
def api_decode_url(packet):
    app.logger.info(f"{req_ipaddr()} send payload via url: {packet}")
    return {'message': src.tw_packet_decoder.hex_str_to_annotation(packet)}

@app.route('/api/v1/decode', methods=["POST"])
def api_decode_form():
    packet = request.form['data']
    if not packet:
        return {'error': 'data can not be empty'}
    app.logger.info(f"{req_ipaddr()} send payload via form: {packet}")
    return {'message': src.tw_packet_decoder.hex_str_to_annotation(packet)}
