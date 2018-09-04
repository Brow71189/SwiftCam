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

import threading
from .buffer import Buffer
import logging
HAS_AMSCOPE_MODULE = True
try:
    from AmScope import amscope
except ModuleNotFoundError:
    HAS_AMSCOPE_MODULE = False
    logging.error('Could not find amscope module. Make sure it is properly installed and can be found via'
                  "from AmScope import amscope.")

class AmScope_camera():
    def __init__(self, url, max_buffer_size=10, max_framerate=60, user=None, password=None):
        self.url = url
        self.user = user
        self.password = password
        self.buffer = Buffer(maxsize=max_buffer_size)
        self.max_framerate = max_framerate
        self._stop_event = threading.Event()
        if HAS_AMSCOPE_MODULE:
            self.amscope_camera = amscope.Toupcam(buffer=self.buffer)
            self._receiver_thread = threading.Thread(target=self.read_from_stream, daemon=True)
            self._receiver_thread.start()

    def close(self):
        self._stop_event.set()
        self._receiver_thread.join(1)
        self.buffer = None

    def read_from_stream(self):
        if hasattr(self, 'amscope_camera'):
            self.amscope_camera.start_live()
            self._stop_event.wait()
            self.amscope_camera.stop_live()