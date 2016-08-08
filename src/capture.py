#!/usr/bin/env python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.
    
    Project:     Autonomous Monitoring System
    File:        capture.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
'''

from multiprocessing import Process, Event, Lock, Queue
from Queue import Full
from time import sleep
import v4l2capture
import select
import cv2
import os
import logging
import numpy as np

FAIL = False

class Capture(Process):

    def __init__(self, out_queue, conf, conf_lock):
        Process.__init__(self)
        self._out_queue = out_queue
        self._stop = Event()
        self._stop.set()
        self._new_conf = Event()
        self._new_conf.clear()
        self._conf_lock = conf_lock
        self._conf = conf
        self._stream = None
        self._device_name = None

    def setDevice(self, device):
        self._device_name = device
    
    def openStream(self):
        logging.debug("Opening stream.")
        try:
            self._stream = v4l2capture.Video_device("/dev/"+self._device_name)
        except IOError as err_pref:
            logging.debug("Could not open default device.")
            devices = [x for x in os.listdir("/dev/") if x.startswith("video")]
            devices.sort()
            for device_new in devices:
                try:
                    self._stream = v4l2capture.Video_device("/dev/"+device_new)
                except IOError as err_new:
                    pass
                else:
                    logging.warning("Device {default} was not available but {new} could be opened.".format(default=self._device_name, new=device_new))
                    self._device_name = device_new
                    return
            raise err_pref
        else:
            return

    def setupStream(self):
        with self._conf_lock:
            self._stream.set_format(self._conf["capture-res"][0], self._conf["capture-res"][1], fourcc='MJPG')
        self._stream.create_buffers(1)
        self._stream.queue_all_buffers()

    def newConf(self):
        self._new_conf.set()

    def run(self):
        self._stop.clear()
        with self._conf_lock:
            conf = self._conf.copy() # Create thread-safe local copy
        
        sleep(float(conf["capture-warmup"])) # Camera warm-up wait
        
        while True :
            if self._stop.is_set():
                break
            if self._new_conf.is_set():
                with self._conf_lock:
                    conf = self._conf.copy()
                self._new_conf.clear()
                logging.debug("New configuration set: {conf}".format(conf=conf))
        
            if conf["capture"]:
                if self._stream is None:
                    if self.tryOpenStream() is FAIL:
                        continue
                try:
                    select.select((self._stream,), (), ())
                    raw = self._stream.read_and_queue()
                except IOError as err_first:
                    self._stream.close()
                    self.tryOpenStream()
                    continue
                
                if raw is None:
                    logging.warning("Grabbed frame is empty.")

                while True:
                    try:
                        self._out_queue.put(cv2.imdecode(np.fromstring(raw, dtype=np.byte), flags=cv2.IMREAD_COLOR), block=False)
                    except Full:
                        self._out_queue.get()
                    else:
                        break
            else:
                sleep(1) # Reduce CPU consumption

        if self._stream is not None:
            self._stream.close()
        logging.info("Thread stopped.")
    
    def tryOpenStream(self):
        try:
            self.openStream()
        except IOError as err:
            with self._conf_lock:
                self._conf["capture"] = False
            self._conf["error"]["capture"] = True
            self._stream = None
            self.newConf()
            logging.error("Capture disabled: could not open stream, no device available.")
            return FAIL
        else:
            self.setupStream()
            self._stream.start()
            return (not FAIL)

    def stop(self):
        self._stop.set()
