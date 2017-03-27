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
            mod = importlib.import_module('.' + camera_module, package='SwiftCam')
            cam = getattr(mod, camera_class)
        except ImportError as detail:
            print(detail)
            print('Could not import camera class {:s} from module {:s}'.format(camera_class, camera_module))
        else:
            _camera_formats[camera_module.split('_')[0].lower()] = cam

import_camera_supplies()

class Camera():
    def __init__(self, **kwargs):
        self.format = kwargs.get('format', 'pyav')
        self.mode = 'Run'
        self.mode_as_index = 0
        self.exposure_ms = 0
        self.binning = 1
        self.sensor_dimensions = (512,512)
        self.readout_area = self.sensor_dimensions
        self.binning_values = [1]
        self.cam = None
        self.url = kwargs.get('url')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.max_framerate = kwargs.get('max_framerate', 0)
        self.frame_number = 0

    def set_exposure_ms(self, exposure_ms, mode_id):
        self.exposure_ms = exposure_ms

    def get_exposure_ms(self, mode_id):
        return self.exposure_ms

    def set_binning(self, binning, mode_id):
        self.binning = binning

    def get_binning(self, mode_id):
        return self.binning

    def get_expected_dimensions(self, binning):
        return self.sensor_dimensions

    def start_live(self):
        if self.url is not None:
            self.cam = _camera_formats[self.format.lower()](self.url, user=self.user, password=self.password,
                                                            max_framerate=self.max_framerate)

    def stop_live(self):
        time.sleep(0.5)
        self.cam.close()

    def acquire_image(self):
        data_element = {}
        data = np.array(self.cam.buffer.get(timeout=10))
        if len(data.shape) > 2 and data.shape[-1] == 3:
            data = data[..., (2, 1, 0)]
        data_element['data'] = data
        data_element['properties'] = {'spatial_calibrations': [{'offset': 0, 'scale': 1, 'units': None}]*2,
                                      'frame_number': self.frame_number}
        self.frame_number += 1
        return data_element

    def acquire_sequence(self, n):
        raise NotImplementedError

    def open_monitor(self):
        raise NotImplementedError

    def open_configuration_interface(self):
        raise NotImplementedError
