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
from PIL import Image
from urllib import request
from .buffer import Buffer

class ACTI_camera():
    def __init__(self, url, max_buffer_size=10, max_framerate=60, user=None, password=None, **kwargs):
        self.url = url
        self.user = user
        self.password = password
        if self.user is not None and self.password is not None and not '@' in self.url:
            spliturl = self.url.split('://')
            concatenated_url = user + ':' + password + '@' + spliturl[-1]
            if len(spliturl) > 1:
                concatenated_url = spliturl[0] + '://' + concatenated_url
            self.url = concatenated_url
        self.buffer = Buffer(maxsize=max_buffer_size)
        self._stop_event = threading.Event()
        self._receiver_thread = threading.Thread(target=self.read_from_stream, daemon=True)
        self._raw_bytes = b''
        self.max_framerate = max_framerate
        self._receiver_thread.start()

    def close(self):
        self._stop_event.set()
        self._receiver_thread.join(1)
        self.buffer = None

    def read_from_stream(self):
        waittime = 1/self.max_framerate if self.max_framerate > 0 else 0
        while not self._stop_event.wait(waittime):
            self.buffer.put(Image.open(request.urlopen(self.url)))