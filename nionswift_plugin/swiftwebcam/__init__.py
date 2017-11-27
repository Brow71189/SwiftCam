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

# standard libraries
import json
import os

#from nion.swift.model import HardwareSource
#from nion.instrumentation.camera_base import CameraHardwareSource

from webcam_utils import webcam
#from . import WebcamCameraManagerImageSource
from nion.utils import Registry

with open(os.path.join(os.path.dirname(__file__), 'config_path.txt')) as config_file_path:
    CONFIG_FILE = os.path.join(config_file_path.readline().strip(), 'webcam_config.json')

class WebcamExtension:

    extension_id = "nion.webcam"

    def __init__(self, api_broker):
        self.api = api_broker.get_api(version='~1.0', ui_version='~1.0')
        self.load_camera_configurations_and_create_cameras()

    def close(self):
        pass

    def register_camera(self, hardware_source_id, display_name, access_data):
        # create the camera
        camera = webcam.Camera(**access_data)
        #camera_map[hardware_source_id] = camera
        # create the hardware source
        #camera_adapter = WebcamCameraManagerImageSource.CameraAdapter(hardware_source_id, display_name, camera)
        #hardware_source = CameraHardwareSource(camera_adapter, None)
        #hardware_source.modes = camera_adapter.modes
        # register it with the manager
        #HardwareSource.HardwareSourceManager().register_hardware_source(hardware_source)
        #self.api.create_hardware_source(camera_adapter)
        camera.camera_id = hardware_source_id
        camera.camera_name = display_name
        camera.camera_type= 'ronchigram'
        Registry.register_component(camera, {'camera_device'})


    def load_camera_configurations_and_create_cameras(self):
        with open(CONFIG_FILE) as config_file:
            camera_parameters = json.load(config_file)
            for camera in camera_parameters:
                cam_id = camera.pop('id')
                name = camera.pop('name', cam_id)
                try:
                    self.register_camera(cam_id, name, camera)
                except Exception as detail:
                    print('Could not register camera {:s}. Reason: {:s}'.format(cam_id, str(detail)))