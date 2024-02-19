#!/bin/bash

source venv/bin/activate || exit 1
pip install -r requirements.txt || exit 1

gunicorn -w 4 -b 127.0.0.1:9822 'main:app'

