#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from extractors import extract_profile, providers

app = Flask(__name__)
app.secret_key = 'ENQG8h47Lk7TD7VR22Ac543ttIEst76I96rI7YFZE69C3m23xVhE6'

app_folder = os.path.split(os.path.abspath(__file__))[0]

@app.route('/_target')
def target():
    """return info from url"""
    target_url = request.args.get('target_url', 'None', type=str)
    info = extract_profile(target_url, providers)
    return jsonify(target_url=target_url, info=str(info))

@app.route('/')
def main_page():
    return render_template('main.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
