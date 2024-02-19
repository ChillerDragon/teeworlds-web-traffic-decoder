#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request

import src.log_config
import src.tw_packet_decoder

app = Flask(__name__)

def req_ipaddr() -> str:
    if not 'HTTP_X_FORWARDED_FOR' in request.environ:
        return request.remote_addr
    return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()

def log_request() -> str:
    app.logger.info(f"{request.method} {request.url} ip={req_ipaddr()} ua={request.headers.get('User-Agent')}")

@app.route('/')
def index():
    return render_template('index.html.j2', foo = "bar")

@app.route('/api/v1/decode/<string:packet>', methods=["POST"])
def api_decode_url(packet):
    log_request()
    app.logger.info(f"{req_ipaddr()} send payload via url: {packet}")
    return {'message': src.tw_packet_decoder.hex_str_to_annotation(packet, True, True)}

@app.route('/api/v1/decode', methods=["POST"])
def api_decode_form():
    log_request()
    packet = request.form['data']
    app.logger.info(request.form)
    if not packet:
        return {'error': 'data can not be empty'}
    app.logger.info(f"{req_ipaddr()} send payload via form: {packet}")
    return {'message': src.tw_packet_decoder.hex_str_to_annotation(packet, 'protocol-6' in request.form, 'protocol-7' in request.form)}
