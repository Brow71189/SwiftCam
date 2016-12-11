# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:59:33 2016

@author: Andi
"""
import time
import numpy as np

from .mjpeg_supply import MJPEG_camera

class Camera():
    __camera_formats = {'mjpeg': MJPEG_camera}

    def __init__(self):
        self.format = 'mjpeg'
        self.mode = 'Run'
        self.mode_as_index = 0
        self.exposure_ms = 30
        self.binning = 1
        self.sensor_dimensions = (512,512)
        self.readout_area = self.sensor_dimensions
        self.cam = None
        self.last_frame_taken = 0
        self.url = 'http://192.168.0.2:8080/video'
        #self.url = 'http://213.193.89.202/axis-cgi/mjpg/video.cgi'
        self.frame_number = 0
    
    def set_exposure_ms(self, exposure_ms, mode_id):
        self.exposure_ms = exposure_ms
    
    def get_exposure_ms(self, mode_id):
        return self.exposure_ms
    
    def set_binning(self, binning, mode_id):
        self.binning = binning
        
    def get_binning(self, mode_id):
        return self.binning
        
    def start_live(self):
        self.cam = self.__camera_formats[self.format](self.url)
    
    def stop_live(self):
        time.sleep(1)
        self.cam.close()
    
    def acquire_image(self):
        now = time.time()
        if now - self.last_frame_taken < self.exposure_ms*0.001:
            time.sleep(self.exposure_ms*0.001 - (now - self.last_frame_taken))
        self.last_frame_taken = now
        data_element = {}
        data_element['data'] = np.array(self.cam.buffer.get(timeout=10))[..., (2, 1, 0)]
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