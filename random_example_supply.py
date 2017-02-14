#MIT License
#
#Copyright (c) 2017 Andreas Mittelberger
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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