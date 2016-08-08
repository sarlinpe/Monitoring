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
                 v4l2capture module.
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

DEVICE_NAME = "video0"
RESOLUTION = (640, 480)
INFO_INTERVAL = 60 # seconds

logFormatter = logging.Formatter(fmt='%(levelname)-8s %(module)-15s %(asctime)-20s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

cam = v4l2capture.Video_device("/dev/"+DEVICE_NAME)
resolution = cam.set_format(RESOLUTION[0], RESOLUTION[1], fourcc='MJPG')
logging.info("Capture resolution: {res}".format(res=resolution))

cam.create_buffers(1)
cam.queue_all_buffers()
cam.start()

cv2.namedWindow('Video feed', 0)
stamp = datetime.datetime.now()

while True:	
	select.select((cam,), (), ())
	raw_data = cam.read_and_queue()
	img = cv2.imdecode(np.fromstring(raw_data, dtype=np.byte), flags=cv2.IMREAD_COLOR)

	if img is None:
		logging.warning("Frame could not be grabbed: empty image.")
		continue

	cv2.imshow('Video feed',img)
	
	if (datetime.datetime.now() - stamp).total_seconds() > INFO_INTERVAL:
		stamp = datetime.datetime.now()
		logging.info("Camera still capturing.")

	if cv2.waitKey(1) >= 0:
        cam.close()
        break

cv2.destroyAllWindows()
