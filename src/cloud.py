#!/usr/bin/env python

'''
    Copyright (c) 2016, Paul-Edouard Sarlin
    All rights reserved.
    
    Project:     Autonomous Monitoring System
    File:        cloud.py
    Date:        2016-08-08
    Author:      Paul-Edouard Sarlin
    Website:	 https://github.com/skydes/monitoring
'''

from multiprocessing import Process, Event, Lock, Queue
from Queue import Empty, Full
import dropbox
import smtplib
from requests.exceptions import ConnectionError, RequestException
from collections import deque
from shutil import copyfile
import os
import time, datetime
import cv2
import logging
import requests.packages.urllib3

BACKUP_PATH = "./image_backup"

class Dropbox(Process):
    
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
        
        self._jpg_buffer = deque([])
        self._client = None
        self._error_time = None
    
    def setClient(self):
        with self._conf_lock:
            conf = self._conf.copy()
        self._client = dropbox.Dropbox(conf["dropbox-token"])
        logging.info("Dropbox account linked.")
    
    def newConf(self):
        self._new_conf.set()

    def run(self):
        self._stop.clear()
        with self._conf_lock:
            conf = self._conf.copy() # Create thread-safe local copy
        
        while True :
            if self._stop.is_set():
                for file in list(self._jpg_buffer):
                    os.remove(file[0])
                break
            if self._new_conf.is_set():
                with self._conf_lock:
                    conf = self._conf.copy()
                self._new_conf.clear()
            
            #if conf["error"]["dropbox"] and ((datetime.datetime.now - last_try).minutes > DROPBOX_TRY_PERIOD):
            
            try:
                (local_path, ts) = self._in_queue.get(block=True, timeout=3)
            except Empty:
                continue

            if conf["dropbox"]:
                if self._client is None:
                    self.setClient()
            
                path = "{base_path}/{timestamp}.jpg".format(base_path=conf["dropbox-path"], timestamp=ts)
                
                try:
                    self.upFile(local_path, path)
                except Error:
                    pass
                else:
                    if error:
                        for files in folder:
                            try:
                                self.upFiles(folder)
                            except Error:
                
                
                
                try: # TODO: handle drobpox-related error (e.g wrong access token)
                    self._client.files_upload(open(local_path, "rb"), path)
                except ConnectionError as err:
                    self.uploadError(True)
                    backup_path = "{base_path}/{timestamp}.jpg".format(base_path=BACKUP_PATH, timestamp=ts)
                    copyfile(local_path, backup_path)
                    logging.error("Dropbox upload failed: no internet connection. Local back-up file created.")
                else:
                    logging.info("File sent to Dropbox.")
                    files = [x for x in os.listdir(BACKUP_PATH)]
                    error = None
                    for file in files:
                        backup_path = "{base_path}/{file}.jpg".format(base_path=BACKUP_PATH, file=file)
                        path = "{base_path}/{file}.jpg".format(base_path=conf["dropbox-path"], file=file)
                        try:
                            self._client.files_upload(open(backup_path, "rb"), path)
                        except ConnectionError as err:
                            error = err
                            self.uploadError(True)
                            logging.error("Could not upload backed-up file.")
                            break
                        else:
                            os.remove(backup_path)
                    if (not files) or (error is None):
                        self.uploadError(False)

            self._jpg_buffer.append((local_path, ts))
            if len(self._jpg_buffer) > int(conf["displayed-frames"]):
                os.remove(self._jpg_buffer[0][0]) # Delete first item to enter in the queue
                self._jpg_buffer.popleft()

            while True:
                try:
                    self._out_queue.put(list(self._jpg_buffer),block=False)
                except Full:
                    self._out_queue.get(block=False)
                else:
                    break

        logging.info("Thread stopped.")
    
    def uploadError(self, set):
        self._error_time = datetime.datetime.now()
        with self._conf_lock:
            self._conf["error"]["dropbox"] = set
            self._conf["error"]["dropbox-time"] = self._error_time.strftime("%A %d %B %Y %I:%M:%S%p")
        self._new_conf.set()
    
    def stop(self):
        self._stop.set()
