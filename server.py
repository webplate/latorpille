#!/usr/bin/python3
# -*- coding: utf-8 -*-
# std lib
import os
# modules
from tinydb import TinyDB, where
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# perso
from extractors import extract_profile, PROVIDERS

app = Flask(__name__)
app.secret_key = 'ENQG8h47Lk7TD7VR22Ac543ttIEst76I96rI7YFZE69C3m23xVhE6'

app_folder = os.path.split(os.path.abspath(__file__))[0]

db = TinyDB(os.path.join(app_folder, 'static/data/db.json'))
#~ db.insert({'int': 1, 'char': 'a'})
#~ print(db.search(where('int') == 1))

def get_matching(info, db):
    '''return list of matching profiles from db
    TODO : sort it'''
    out = []
    s = db.search((where('name') == info['name'])
      & (where('profile_url') == info['profile_url']))
    for profile in s:
        if not profile in out:
            out.append(profile)
    return out

@app.route('/_target')
def target():
    """return info from url AJAX way"""
    target_url = request.args.get('target_url', 'None', type=str)
    contact_info = request.args.get('contact_info', 'None', type=str)
    if target_url != None:
        info = extract_profile(target_url, PROVIDERS)
        if info != None:
            # should we add contact info in db ?
            if contact_info != 'None':
                info.update({'contact_info': contact_info})
                if not info in db.all():
                    db.insert(info)
            # is this profile matching an item in db?
            matches = get_matching(info, db)
            if len(matches) > 0:
                match = matches[0]
                return jsonify(profile_found=True,
                    target_url=target_url,
                    name=match['name'],
                    photo_url=match['photo_url'],
                    domain=match['domain'],
                    contact_found=True,
                    contact_info=match['contact_info'])
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

@app.route('/')
def main_page():
    return render_template('main.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
