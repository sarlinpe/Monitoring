#!/usr/bin/env python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.

    Project:     Autonomous Monitoring System
    File:        main.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
'''

from multiprocessing import Queue, Lock
from Queue import Empty
from rocket import Rocket
from threading import Thread
import signal
import time
import cv2
import json
import logging, logging.handlers

from capture import Capture
from processing import Processing
from cloud import Dropbox
from server import *

QUEUE_MAXSIZE = 10
PORT = 8000

# Setup logging
logFormatter = logging.Formatter(fmt='%(levelname)-8s %(module)-15s %(asctime)-20s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.handlers.RotatingFileHandler("./log/app.log", maxBytes=30000, backupCount=5)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# Setup configuration
with open("conf.json") as json_file:
    app.conf.update(json.load(json_file))

# Initialize and configure threads
app.pre_queue = Queue(maxsize=QUEUE_MAXSIZE)
app.post_queue = Queue(maxsize=QUEUE_MAXSIZE)
app.server_queue = Queue(maxsize=1)
app.conf_lock = Lock()

# Make main procezs ignore SIGNINT
original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

app.capture_th = Capture(app.pre_queue, app.conf, app.conf_lock)
app.processing_th = Processing(app.pre_queue, app.post_queue, app.conf, app.conf_lock)
app.dropbox_th = Dropbox(app.post_queue, app.server_queue, app.conf, app.conf_lock)

app.capture_th.setDevice("video0")
    
# Launch threads
app.dropbox_th.start()
app.processing_th.start()
app.capture_th.start()
logging.info("Threads started.")

# Restore SIGNINT handler
signal.signal(signal.SIGINT, original_sigint_handler)

# Launch server
rocket_server = Rocket(('localhost', PORT), 'wsgi', {'wsgi_app': app})
app.server_th = Thread(target=rocket_server.start, name='rocket_server')
app.server_th.start()
logging.getLogger("Rocket").setLevel(logging.INFO)
logging.info("Server started.")

try:
    while app.server_th.is_alive():
        app.server_th.join(1)
except (KeyboardInterrupt, SystemExit):
    rocket_server.stop()
    logging.info("Server stopped.")

app.capture_th.stop()
app.capture_th.join()
app.processing_th.stop()
app.processing_th.join()
app.dropbox_th.stop()
app.dropbox_th.join()

cv2.destroyAllWindows()
