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
    """return info from url AJAX way"""
    target_url = request.args.get('target_url', 'None', type=str)
    info = extract_profile(target_url, providers)
    if info != None:
        print("YOOOOOOO")
        # is this profile matching an item in db?
        if False:
            return jsonify(profile_found=True,
                target_url=target_url,
                name=info['name'],
                photo_url=info['photo_url'],
                domain=info['domain'],
                contact_found=True,
                contact_info='0102032156')
        else:
            return jsonify(profile_found=True,
                target_url=target_url,
                name=info['name'],
                photo_url=info['photo_url'],
                domain=info['domain'],
                contact_found=False)
    else:
        return jsonify(profile_found=False,
            target_url=target_url)

@app.route('/target')
def result():
    """return info from url"""
    target_url = request.args.get('url', 'None', type=str)
    info = extract_profile(target_url, providers)
    return render_template('result.html',
        target_url=target_url,
        info=str(info))


@app.route('/')
def main_page():
    return render_template('main.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
