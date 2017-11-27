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

import urllib
import io
from PIL import Image
import threading
import time
import numpy as np
from .buffer import Buffer

class MJPEG_camera():
    def __init__(self, url, max_buffer_size=10, max_framerate=60, user=None, password=None):
        self.url = url
        self.user = user
        self.password = password
        self.buffer = Buffer(maxsize=max_buffer_size)
        if self.user is not None and self.password is not None:
            self.passman = urllib.request.HTTPPasswordMgrWithPriorAuth()
            self.passman.add_password(None, self.url, self.user, self.password)
            urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(self.passman)))

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
        #counter = 0
        while not self._stop_event.is_set():
            self._raw_bytes += self._stream.read(1024)
            a = self._raw_bytes.find(b'\xff\xd8')
            b = self._raw_bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = self._raw_bytes[a:b+2]
                self._raw_bytes= self._raw_bytes[b+2:]
                bytes_image = io.BytesIO(jpg)
                self.buffer.put(Image.open(bytes_image))
                now = time.time()
                frametimes.append(now - last_run)
                frametimes.pop(0)
                last_run = now
#                if counter > 10:
#                    print('Current fps: {:.2f}'.format(1/np.mean(frametimes)), end='')
#                    counter = 0
#                counter += 1
                sleeptime = waittime - (np.mean(frametimes) - waittime) - 0.001
                time.sleep(sleeptime if sleeptime > 0 else 0)
                #time.sleep(waittime)
