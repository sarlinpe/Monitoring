#!/usr/bin/env python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.
    
    Project:     Autonomous Monitoring System
    File:        server.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
'''

import bottle
from multiprocessing import Queue, Lock, Manager
from Queue import Empty
import logging

app = bottle.Bottle()
app.frames_list = []
app.conf = Manager().dict()

@app.route('/')
def home():
    try:
        app.frames_list = app.server_queue.get(block=False)
    except Empty:
        pass
    with app.conf_lock:
        return bottle.template('temp_bootstrap_home', conf=app.conf, frames_list=app.frames_list)

@app.route('/toggle/')
def toggle():
    with app.conf_lock:
    	app.conf["capture"] = not app.conf["capture"]
        logging.debug("Capture toggled: {conf}".format(conf=app.conf))
    app.capture_th.newConf()
    bottle.redirect("/") # TODO: don't redirect but display if activation has been successful

@app.route('/settings/')
def settings():
    with app.conf_lock:
        return bottle.template('temp_bootstrap_settings', conf=app.conf)

@app.route('/log/')
def settings():
    with app.conf_lock:
        return bottle.template('temp_bootstrap_log', conf=app.conf, file=open("./log/app.log","r"))

@app.post('/settings/')
def update_settings():
    with app.conf_lock:
        app.conf.update(dict(bottle.request.forms))
        app.conf["dropbox"] = (bottle.request.forms.get("dropbox") == "True")
    logging.info("New settings saved.")
    
    app.capture_th.newConf()
    app.processing_th.newConf()
    app.dropbox_th.newConf()
    # TODO check if the new conf could be taken into account
    
    bottle.redirect("/settings/")

@app.get('/static/:path#.+#')
def server_static(path):
    return bottle.static_file(path, root="./")

@app.get('/temp/:path#.+#')
def server_captures(path):
    try:
        return bottle.static_file(path, root="./temp")
    except OSError as err:
        logging.error("Error accessing static file: {message}".format(message=err.strerror))
        return None

@app.get('/favicon.ico')
def get_favicon():
    logging.info("Favicon requested.")
    return server_static('./views/favicon.png')
