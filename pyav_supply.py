# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:44:42 2017

@author: mittelberger2
"""

import av
import threading
import queue
import numpy as np

class Buffer(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize=maxsize)

    def get(self, block=True, timeout=None):
        obj = super().get(block=block, timeout=timeout)
        self.task_done()
        return obj


class PyAV_camera():
    def __init__(self, url, max_buffer_size=10, user=None, password=None):
        self.url = url
        self.user = user
        self.password = password
        self.buffer = Buffer(maxsize=max_buffer_size)
        self.container = av.open(url)
        self.video_stream = next(s for s in self.container.streams if s.type == 'video')
        self._stop_event = threading.Event()
        self._receiver_thread = threading.Thread(target=self.read_from_stream, daemon=True)
        self._receiver_thread.start()
        
    def close(self):
        self._stop_event.set()
        self._receiver_thread.join(1)
        self.buffer = None

    def read_from_stream(self):
        for packet in self.container.demux(self.video_stream):
            if self._stop_event.is_set():
                break
            frame = packet.decode_one()
            if frame is not None:
                frame = frame.to_image()
                if self.buffer.full():
                    self.buffer.get()
                self.buffer.put(np.array(frame))