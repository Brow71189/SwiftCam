# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 14:29:12 2017

@author: ASUser
"""
import queue
import threading
from PIL import Image
from urllib import request


class Buffer(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    def get(self, block=True, timeout=None):
        obj = super().get(block=block, timeout=timeout)
        self.task_done()
        return obj

    def put(self, obj, block=True, timeout=None):
        if self.full():
            self.get()
        super().put(obj, block=block, timeout=None)

class ACTI_camera():
    def __init__(self, url, max_buffer_size=10, max_framerate=60, user=None, password=None):
        self.url = url
        self.user = user
        self.password = password
        #self.buffer = queue.Queue(maxsize=max_buffer_size)
        self.buffer = Buffer(maxsize=max_buffer_size)
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
        while not self._stop_event.wait(waittime):
            self.buffer.put(Image.open(request.urlopen(self.url)))