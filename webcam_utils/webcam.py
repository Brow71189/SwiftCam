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

import time
import numpy as np
import os
import pyclbr
import importlib

_camera_formats = dict()

def import_camera_supplies():
    dirlist = os.listdir(os.path.dirname(__file__))
    matched_dirlist = []
    for name in dirlist:
        if os.path.splitext(name)[1] == '.py' and os.path.splitext(name.lower())[0].endswith('_supply'):
            matched_dirlist.append(os.path.splitext(name)[0])

    camera_classes = []
    for name in matched_dirlist:
        try:
            contents = pyclbr.readmodule(name, path=[os.path.dirname(__file__)])
        except AttributeError:
            print('Could not read module ' + name)
        else:
            for classname in contents.keys():
                if classname.lower().endswith('_camera'):
                    camera_classes.append((name, classname))

    for camera_module, camera_class in camera_classes:
        try:
            mod = importlib.import_module('.' + camera_module, package='webcam_utils')
            cam = getattr(mod, camera_class)
        except ImportError as detail:
            print(detail)
            print('Could not import camera class {:s} from module {:s}'.format(camera_class, camera_module))
        else:
            _camera_formats[camera_module.split('_')[0].lower()] = cam

import_camera_supplies()

class Camera:
    def __init__(self, **kwargs):
        self.cam = None
        self.format = kwargs.get('format', 'pyav')
        self.url = kwargs.get('url')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.max_framerate = kwargs.get('max_framerate', 0)
        self.options = kwargs.get('options', '')

    def start_acquisition(self):
        if self.url is not None:
            self.cam = _camera_formats[self.format.lower()](self.url, user=self.user, password=self.password,
                                                            max_framerate=self.max_framerate, options=self.options)

    def acquire_data(self):
        data = np.array(self.cam.buffer.get(timeout=10))
        if len(data.shape) > 2 and data.shape[-1] == 3:
            data = data[..., (2, 1, 0)]
        return data

    def stop_acquisition(self):
        time.sleep(0.5)
        self.cam.close()

    def update_settings(self, settings: dict) -> None:
        self.format = settings.get('format', 'pyav')
        self.url = settings.get('url')
        self.user = settings.get('user')
        self.password = settings.get('password')
        self.max_framerate = settings.get('max_framerate', 0)
        self.options = settings.get('options', '')