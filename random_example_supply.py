# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 09:14:41 2017

@author: Andi
"""

from .buffer import Buffer
import numpy as np
import threading

class Random_Example_camera():
    def __init__(self, url, user=None, password=None, max_framerate=30):
        self.url = url
        self.user = user
        self.password = password
        self.max_framerate = max_framerate
        self.buffer = Buffer()
        self._receiver_thread = threading.Thread(target=self.receive_from_stream, daemon=True)
        self._stop_event = threading.Event()
        self._receiver_thread.start()
        
    def close(self):
        self._stop_event.set()
        self._receiver_thread.join(1)
        self.buffer = None
        
    def receive_from_stream(self):
        waittime = 1/self.max_framerate if self.max_framerate > 0 else 0
        while not self._stop_event.wait(waittime):
            image = (np.random.rand(512,512, 3) * 256).astype(np.uint8)
            self.buffer.put(image)           