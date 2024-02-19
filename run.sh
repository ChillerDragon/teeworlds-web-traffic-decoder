#!/bin/sh

gunicorn -w 4 'main:app'

