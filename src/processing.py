#!/usr/bin/env python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.
    
    Project:     Autonomous Monitoring System
    File:        processing.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
'''

from multiprocessing import Process, Event, Lock, Queue
from Queue import Empty
import cv2
import time, datetime
import logging
import uuid, os

class Processing(Process):
    
    def __init__(self, in_queue, out_queue, conf, conf_lock):
        Process.__init__(self)
        self._in_queue = in_queue
        self._out_queue = out_queue
        self._stop = Event()
        self._stop.set()
        self._new_conf = Event()
        self._new_conf.clear()
        self._conf_lock = conf_lock
        self._conf = conf

    def newConf(self):
        self._new_conf.set()

    def run(self):
        self._stop.clear()
        average = None
        last_up = datetime.datetime.now()
        motion_counter = 0
        with self._conf_lock:
            conf = self._conf.copy() # Create thread-safe local copy
        if conf["debug"]:
                cv2.namedWindow("Display", 0)
	        
        while True :
            if self._stop.is_set():
                break
            if self._new_conf.is_set():
                with self._conf_lock:
                    conf = self._conf.copy()
                self._new_conf.clear()
            
            # Fetch frame
            try:
                frame = self._in_queue.get(block=True, timeout=3)
            except Empty:
                continue
            while not self._in_queue.empty():
                self._in_queue.get()

            # Process frame
            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            if average is None:
                average = gray.copy().astype("float")
                self.sendCloud(frame, ts)
                logging.info("Sending first frame.")
                continue
            
            cv2.accumulateWeighted(gray, average, 0.5)
            delta = cv2.absdiff(gray, cv2.convertScaleAbs(average))
            thresh = cv2.threshold(delta, int(conf["proc-motion-thresh"]), 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            motion = False
            for c in contours:
                if cv2.contourArea(c) < int(conf["proc-min-area"]):
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                motion = True
            cv2.putText(frame, ts, (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 1)

            # Select interesting frames
            if motion and ((timestamp - last_up).seconds > float(conf["proc-min-delay"])):
                motion_counter += 1
                if motion_counter > int(conf["proc-min-motion-frames"]):
                    logging.info("Motion detected.")
                    self.sendCloud(frame, ts)
                    montion_counter = 0
                    last_up = timestamp
            else:
                motion_counter = 0

            if conf["debug"]:
                cv2.imshow("Display", frame)
                cv2.waitKey(1)
        
        cv2.destroyWindow("Display")
        logging.info("Thread stopped.")
        
    def sendCloud(self, img, ts):
        path = "temp/{rand}.jpg".format(rand=str(uuid.uuid4()))
        cv2.imwrite(path, img)
        self._out_queue.put((path,ts)) # TODO: exception handling if full

    def stop(self):
        self._stop.set()
