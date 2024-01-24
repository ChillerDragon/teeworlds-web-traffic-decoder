#!/usr/bin/env python3

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html.j2', foo = "bar")

@app.route('/api/v1/decode/<string:packet>', methods=["POST"])
def api_set_gametile(packet):
    app.logger.info(f"got packet: {packet}")
    return {'status': 'ok'}
