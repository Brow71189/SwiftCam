# -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""

import setuptools

setuptools.setup(
    name="SwiftCam",
    version="0.2.0",
    author="Andreas Mittelberger",
    author_email="Brow71189@gmail.com",
    description="Webcam Support for Nion Swift",
    url="https://github.com/Brow71189/SwiftCam",
    packages=["webcam_utils", "nionswift_plugin.swiftwebcam"],
    license='MIT',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.5",
    ],
    include_package_data=True,
    python_requires='~=3.5',
)
