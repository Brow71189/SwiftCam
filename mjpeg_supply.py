# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 11:01:24 2016

@author: Andi
"""

#import cv2
import urllib 
#import numpy as np
import io
from PIL import Image
#import matplotlib.pyplot as plt
import threading
import time
#import copy
import queue
import numpy as np

#stream=urllib.request.urlopen('http://213.193.89.202/axis-cgi/mjpg/video.cgi')
#stream=urllib.request.urlopen('http://192.168.0.2:8080/video')
#r_bytes=b''
#fig = plt.figure()
#ax = fig.add_subplot(111)
#q = queue.Queue(maxsize=100)
#first_run = True
#showim = None
#
#def update_plt():
#    global ax, showim, first_run
#    while True:
#        im = q.get()
#        if first_run:
#            showim = ax.imshow(im)
#            first_run = False
#        else:
#            showim.set_data(im)
#        q.task_done()
#        time.sleep(0.01)
#
#def read_from_stream():
#    global r_bytes
#    while True:
#        r_bytes+=stream.read(1024)
#        a = r_bytes.find(b'\xff\xd8')
#        b = r_bytes.find(b'\xff\xd9')
#        if a!=-1 and b!=-1:        
#            jpg = r_bytes[a:b+2]
#            r_bytes= r_bytes[b+2:]
#            #break
#            b_im = io.BytesIO(jpg)
#            q.put(copy.copy(Image.open(b_im)))
#            #plt.imshow(im)
#        
#        #i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
#        #cv2.imshow('i',i)
#        #if cv2.waitKey(1) ==27:
#        #    exit(0)

#t1 = threading.Thread(target=read_from_stream, daemon=True).start()
#t2 = threading.Thread(target=update_plt, daemon=True).start()
class Buffer(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)
    
    def get(self, block=True, timeout=None):
        obj = super().get(block=block, timeout=timeout)
        self.task_done()
        return obj

class MJPEG_camera():
    def __init__(self, url, max_buffer_size=10, max_framerate=60):
        self.url = url
        #self.buffer = queue.Queue(maxsize=max_buffer_size)
        self.buffer = Buffer(maxsize=max_buffer_size)
        self._stream = urllib.request.urlopen(self.url)
        self._stop_event = threading.Event()
        self._receiver_thread = threading.Thread(target=self.read_from_stream, daemon=True)
        self._raw_bytes = b''
        self.max_framerate = max_framerate
        
        self._receiver_thread.start()

    def close(self):
        self._stop_event.set()
        self._receiver_thread.join(1)
        self._stream.close()
        self.buffer = None
        
    def read_from_stream(self):
        waittime = 1/self.max_framerate if self.max_framerate > 0 else 0
        last_run  = time.time()
        frametimes = [0,0,0,0,0]
        counter = 0
        while not self._stop_event.is_set():
            self._raw_bytes += self._stream.read(1024)
            a = self._raw_bytes.find(b'\xff\xd8')
            b = self._raw_bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:        
                jpg = self._raw_bytes[a:b+2]
                self._raw_bytes= self._raw_bytes[b+2:]
                bytes_image = io.BytesIO(jpg)
                if self.buffer.full():
                    self.buffer.get()
                self.buffer.put(Image.open(bytes_image))
                now = time.time()
                frametimes.append(now - last_run)
                frametimes.pop(0)
                last_run = now
                if counter > 10:
                    print('Current fps: {:.2f}'.format(1/np.mean(frametimes)), end='')
                    counter = 0
                counter += 1
                sleeptime = waittime - (np.mean(frametimes) - waittime) - 0.001
                time.sleep(sleeptime if sleeptime > 0 else 0)
                #time.sleep(waittime)
        