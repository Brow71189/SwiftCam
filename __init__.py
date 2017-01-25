"""
Created on Fri Aug  5 09:16:23 2016

@author: mittelberger
"""

# standard libraries
import json
import logging
import os
try:
    from nion.swift.model import HardwareSource
    from Camera import CameraHardwareSource
except:
    pass
from . import webcam
from . import WebcamCameraManagerImageSource

#camera_map = dict()
#__all__ = ["camera_map"]
#__all__.append("WebcamCameraManagerImageSource")

CONFIG_FILE = 'webcam_config.json'

def register_camera(hardware_source_id, display_name, access_data):
    # create the camera
    camera = webcam.Camera(**access_data)
    #camera_map[hardware_source_id] = camera
    # create the hardware source
    camera_adapter = WebcamCameraManagerImageSource.CameraAdapter(hardware_source_id, display_name, camera)
    hardware_source = CameraHardwareSource.CameraHardwareSource(camera_adapter, None)
    hardware_source.modes = camera_adapter.modes
    # register it with the manager
    HardwareSource.HardwareSourceManager().register_hardware_source(hardware_source)

def load_camera_configurations_and_create_cameras():
    with open(os.path.join(os.path.dirname(__file__), CONFIG_FILE)) as config_file:
        camera_parameters = json.load(config_file)
        for camera in camera_parameters:
            cam_id = camera.pop('id')
            name = camera.pop('name', cam_id)
            try:
                register_camera(cam_id, name, camera)
            except Exception as detail:
                print('Could not register camera {:s}. Reason: {:s}'.format(cam_id, str(detail)))
                
load_camera_configurations_and_create_cameras()
                
#access_data1 = {'url': 'http://131.130.31.203/cgi-bin/encoder?USER=admin&PWD=123456&SNAPSHOT', 'format': 'acti'}
#__register_camera('nionppcam', 'None', 'Polepiece Camera', access_data1)
#access_data2 = {'url': 'http://131.130.31.202/cgi-bin/encoder?USER=admin&PWD=123456&SNAPSHOT', 'format': 'acti'}
#__register_camera('nionllcam', 'ronchigram', 'Loadlock Camera', access_data2)
#access_data3 = {'url': 'http://131.130.31.214/channel2', 'format': 'mjpeg', 'user': 'admin', 'password': 'admin'}
#__register_camera('nionppcam2', 'ronchigram', 'Polepiece Camera 2', access_data3)

#access_data1 = {'url': 'http://213.193.89.202/axis-cgi/mjpg/video.cgi', 'format': 'mjpeg'}
#__register_camera('webcam_mjpeg', 'ronchigram', 'MJPEG Webcam', access_data1)
#access_data2 = {'url': 'rtsp://mm2.pcslab.com/mm/7h1500.mp4', 'format': 'pyav'}
#__register_camera('webcam_pyav', 'ronchigram', 'PyAV Webcam', access_data2)
#access_data3 = {'url': 'https://streamsrv60.feratel.co.at/streams/1/05604_5888ab1f-d4d7Vid.mp4?dcsdesign=feratel4', 'format': 'pyav'}
#__register_camera('webcam_ski', 'ronchigram', 'Ski Webcam', access_data3)
#camera_data = [{'name': 'MJPEG Webcam', 'id': 'webcam_mjpeg', 'url': 'http://213.193.89.202/axis-cgi/mjpg/video.cgi', 'format': 'mjpeg'},
#               {'name': 'PyAV Webcam', 'id': 'webcam_pyav', 'url': 'rtsp://mm2.pcslab.com/mm/7h1500.mp4', 'format': 'pyav'},
#               {'name': 'Ski Webcam', 'id': 'webcam_ski', 'url': 'https://streamsrv60.feratel.co.at/streams/1/05604_5888ab1f-d4d7Vid.mp4?dcsdesign=feratel4', 'format': 'pyav'}]