# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools
import os
from pathlib import Path
from shutil import copy2

home = str(Path.home())
config_path = os.path.join(home, 'SwiftCam')
with open('config_path.txt', 'w') as config_path_file:
    config_path_file.write(config_path)

setuptools.setup(
    name="SwiftCam",
    version="0.0.1",
    author="Andreas Mittelberger",
    author_email="Brow71189@gmail.com",
    description="Webcam Support for Nion Swift",
    url="https://github.com/Brow71189/SwiftCam",
    packages=["webcam_utils", "nionswift_plugin.swiftwebcam"],
    data_files=[('nionswift_plugin/swiftwebcam', ['config_path.txt'])],
    license='MIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True,
    python_requires='~=3.5',
)

os.makedirs(config_path, exist_ok=True)
copy2('webcam_config.json.example', config_path)
print('\n################################################################\n')
print(('Copied "webcam_config.json.example" to {}. You have to rename it to "webcam_config.json" and put in your ' +
      'connection info. Alternatively you can copy an existing config file to this location.').format(config_path))
print('\n################################################################\n')