#from . import EELSImageSource

#def run():
#    EELSImageSource.run()

#from . import configuration_interface
#from . import EELScam_GUI

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:16:23 2016

@author: mittelberger
"""

# standard libraries
#import configparser
import logging
#import os
#import traceback

# third party libraries
# None

# local libraries
from nion.swift.model import HardwareSource
from Camera import CameraHardwareSource
from . import webcam

camera_map = dict()

__all__ = ["camera_map"]

#class Camera:
#    def __init__(self):
#        self.on_low_level_parameter_changed = None
#    
#    def get_exposure_ms(self, mode):
#        print(mode)
#        return 1
#    
#    def get_binning(self, mode):
#        return 1
#    
#    def mode_as_index(self, mode):
#        return 1

# package imports
try:
    #import _nioncore
    #import _nioncameramanager

    from . import WebcamCameraManagerImageSource
    __all__.append("WebcamCameraManagerImageSource")

    def __register_camera(hardware_source_id, camera_category, display_name, access_data):
        # function to help with logging
#        def periodic_logger():
#            messages = _nioncore.get_log_messages()
#            data_elements = _nioncore.get_log_images_as_data_elements()
#            return messages, data_elements
        # create the camera
        camera = webcam.Camera(**access_data) #_nioncameramanager.NCMCamera(camera_id=hardware_source_id)
        camera_map[hardware_source_id] = camera
        # create the hardware source
        camera_adapter = WebcamCameraManagerImageSource.CameraAdapter(hardware_source_id, camera_category, display_name, camera)
        hardware_source = CameraHardwareSource.CameraHardwareSource(camera_adapter, None)#periodic_logger)
        hardware_source.modes = camera_adapter.modes
        #hardware_source.acquire_sequence = camera.acquire_sequence
        # register it with the manager
        HardwareSource.HardwareSourceManager().register_hardware_source(hardware_source)

#    def __find_cameras():
#        _nioncameramanager.register_cameras()
#        instances = _nioncameramanager.NionCameraManagerPy.CCameraManager_GetInstance().GetCameraInstances()
#        logging.info("Looking for cam.ini files %s", _nioncameramanager.NionCameraManagerPy.CCameraManager_GetInstance().GetRootConfigPath())
#        # instances is a wrapped SWIG object (vector of shared pointers.)  It doesn't wrap all that nicely, hence the
#        # somewhat strange loop here.
#        errors = []
#        for i in range(instances.size()):
#            try:
#                hardware_id = instances[i].GetCameraID()
#                camera_name = instances[i].GetCameraName()
#                #camera_category = instances[i].GetCameraCategory()
#                camera_category = "eels"
#                __register_camera(hardware_id, camera_category, camera_name)
#                logging.info("Found camera %s %s %s", hardware_id, camera_name, camera_category)
#            except RuntimeError as e:
#                errors.append(e)
#        if len(errors):
#            [logging.warn(error) for error in errors]

    # find cameras automatically
    #__find_cameras()
    access_data1 = {'url': 'http://213.193.89.202/axis-cgi/mjpg/video.cgi', 'format': 'mjpeg'}
    __register_camera('webcam_mjpeg', 'ronchigram', 'MJPEG Webcam', access_data1)
    access_data2 = {'url': 'rtsp://mm2.pcslab.com/mm/7h1500.mp4', 'format': 'pyav'}
    __register_camera('webcam_pyav', 'ronchigram', 'PyAV Webcam', access_data2)

except ImportError as detail:
    logging.warning("Could not import camera manager hardware sources. Reason: {:s}".format(str(detail)))


