SwiftCam
===============

This python package provides a simple interface for showing webcam streams within Nion Swift¹. Currently it supports
all streams that can be received by ffmpeg. This is realized via the package "pyav"², which provides python bindings
for ffmpeg.


Installation and Requirements
=============================

Requirements
------------
* python 3.5
* numpy
* PIL (for python 3 PIL is available as the fork Pillow)
* PyAV² (optional, without pyav only mjpeg streams and streams from acti tcm 4201 cameras can be played)

Installation
------------
After having installed all requirements just download the source code, unzip it and copy it into your Nion Swift
plugins location. The correct location for your operating system is described on the following website:
http://nion.com/swift/developer/introduction.html#extension-locations


Usage
=====

Adding a camera
---------------

In the package there is a file included called "webcam_config.json.example". Copy or rename it to webcam_config.json.
In the json file, each object represents one camera. The easiest way to get it to work is to alter the example file.
The tags that can be specified for a camera are the following:

* "url": The url of your stream. If you are using the format "pyav" you can specify username and password to the stream
         directly in the url. For "mjpeg" you have to use the "user" and "password" tags.

* "id": The ID which is used by Nion Swift to identify your camera.
         
* "format": optional, defaults to "pyav". Currently supported are "pyav", "mjpeg", "acti" and "random".
  - "pyav" will try to play the stream with PyAV (which is essentially ffmepg).
  - "mjpeg" will treat the stream as "MJPEG".
  - "acti" is a special implementation to support acti tcm 4201 cameras as they are used by Nion for some of thei
           microscopes.
  - "random" will enable the example camera implementation which just shows random noise. This is useful to test your
             installation.

* "name": optional, defaults to "id". This is the name under which the camera will be displayed in Nion Swift.
* "user": optional, the username if your stream requires one.
* "password": optional, the password for your stream if it is protected.
* "max_framerate": optional, limits the framerate of the stream to the value given here. This is useful if you
                   heavy CPU load on your computer with a stream.

Implementing new camera formats
-------------------------------

If your stream is not supported by the handlers shipped with this code it is easy to implement your own one. New
handlers will be detected automatically and will be available after a restart of NionSwift. There a three requirements
for a handler to be correctly recognized:

1. The new python module must be in the same folder as all other source code files of this package
2. The filename of the new module must end with "_supply.py"
3. The new module must implement a class whose name ends with "_camera"

The easiest way is to take the random example camera "random_example_supply.py" and edit it. As you can see there, the
camera is immediately started when an instance of the "_camera" class is created. The "__init__" method has to take the
url as a first argument and accept the keyword arguments "user", "password" and "max_framerate".
Passing images is done by a buffer class of which the camera has to hold an instance under the attribute "buffer". The
easiest way is to use the buffer code shipped with this package. Images in the buffer have to be either numpy arrays
or PIL Image objects. They can be sent to the buffer by calling "buffer.put(image)".
The camera class also has to implement a method "close" which should take care of stopping the loop that puts images
into the buffer.

¹ www.nion.com/swift

²https://github.com/mikeboers/PyAV