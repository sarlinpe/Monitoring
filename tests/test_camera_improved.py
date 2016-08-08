#! /usr/bin/python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.
    
    Project:     Autonomous Monitoring System
    File:        test_camera_simple.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
    
    Description: Testing basic polling capture using the
                 v4l2capture module, handling camera errors.
'''

import os
import cv2
import sys
import numpy as np
import datetime
import time
import select
import v4l2capture
import logging

RESOLUTION = (640, 480)
INFO_INTERVAL = 60 # seconds

stream = None
device_name = "video0"

logFormatter = logging.Formatter(fmt='%(levelname)-8s %(module)-15s %(asctime)-20s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

def openStream():
    global stream, device_name
    
    logging.info("Opening stream.")
    try:
        stream = v4l2capture.Video_device("/dev/"+device_name)
    except IOError as err_pref:
        logging.warning("Could not open default device.")
        devices = [x for x in os.listdir("/dev/") if x.startswith("video")]
        devices.sort()
        for device_new in devices:
            try:
                stream = v4l2capture.Video_device("/dev/"+device_new)
            except IOError as err_new:
                pass
            else:
                logging.error("Device {default} was not available but {new} could be opened.".format(default=device_name, new=device_new))
                device_name = device_new
                return
        raise err_pref
    else:
        return

def setupStream():
    resolution = stream.set_format(RESOLUTION[0], RESOLUTION[1], fourcc='MJPG')
    logging.info("Capture resolution: {res}".format(res=resolution))
    stream.create_buffers(1)
    stream.queue_all_buffers()

cv2.namedWindow('Video feed', 0)
stamp = datetime.datetime.now()

while True:
    if stream is None:
        try:
            openStream()
        except IOError as err:
            logging.error("{err}".format(err=err))
            break
        else:
            setupStream()
            stream.start()

    try:
        select.select((stream,), (), ())
        raw_data = stream.read_and_queue()
    except IOError as err:
        logging.warning("{err}".format(err=err))
        stream = None
        continue
        
    img = cv2.imdecode(np.fromstring(raw_data, dtype=np.byte), flags=cv2.IMREAD_COLOR)

    if img is None:
		logging.warning("Frame could not be grabbed: empty image.")
        continue

    cv2.imshow('Video feed',img)
	
    if (datetime.datetime.now() - stamp).total_seconds() > INFO_INTERVAL:
        stamp = datetime.datetime.now()
		logging.info("Camera still capturing.")

    if cv2.waitKey(1) >= 0:
        stream.close()
        break

cv2.destroyAllWindows()
