SwiftCam
===============

This python package provides a simple interface for showing webcam streams within Nion Swift¹. Currently it supports
all streams that can be received by ffmpeg. This is realized via the package "pyav"², which provides python bindings
for ffmpeg. Without pyav it supports some specific stream formats such as mjpeg and can also be extended by the user to support new formats (see later sections for mor details).


Installation and Requirements
=============================

Requirements
------------
* python >=3.5 (lower versions might work but are untested)
* nionswift-video-capture
* numpy (should be already there if you've installed Swift)
* PIL (for python 3, PIL is available as the fork Pillow)
* PyAV² (optional, without pyav only certain stream formats such as mjpeg streams can be played)
* PyAmScope³ (optional, only needed if you want to use AmScope or Touptek cameras)

Installation
------------
The recommended way is to use git to clone the repository as this makes receiving updates easy:
```bash
git clone https://github.com/Brow71189/SwiftCam
```

If you do not want to use git you can also use github's "download as zip" function and extract the code afterwards.

Once you have the repository on your computer, enter the folder "SwiftCam" and run the following from a terminal:

```bash
python setup.py install
```

It is important to run this command with __exactly__ the python version that you use for running Swift. If you installed Swift according to the online documentation (https://nionswift.readthedocs.io/en/stable/installation.html#installation) you should run `conda activate nionswift` in your terminal before running the above command.

Usage
=====

Adding a camera
---------------

Within Swift click on Edit -> Preferences and in the window that pops up select "SwiftCam" from the drop-down menu at the bottom. By clicking on "New" you can add a new camera and you can set up the following parameters in the user interface. Remember to click on "Apply" after changing any of the parameters.

* "url": The url of your stream. If you are using the format "pyav" you can specify username and password to the stream directly in the url. For "mjpeg" you have to use the "user" and "password" tags.

* "id": The ID which is used by Nion Swift to identify your camera.
         
* "format": optional, defaults to "pyav". Currently supported are "pyav", "mjpeg", "acti" and "random".
  - "pyav" will try to play the stream with PyAV (which is essentially ffmepg).
  - "mjpeg" will treat the stream as "MJPEG".
  - "acti" is a special implementation to support acti tcm 4201 cameras as they are used by Nion for some of their microscopes.
  - "amscope" is a special implementation for AmScope and Touptek cameras. 
  - "random" will enable the example camera implementation which just shows random noise. This is useful to test your installation.

* "name": optional, defaults to "id". This is the name under which the camera will be displayed in Nion Swift.
* "user": optional, the username if your stream requires one.
* "password": optional, the password for your stream if it is protected.
* "max_framerate": optional, limits the framerate of the stream to the value given here. This is useful if you encounter heavy CPU load on your computer with a stream.
* "options": optional, additional options sent to the webcam driver.

Implementing new camera formats
-------------------------------

If your stream is not supported by the handlers shipped with this code it is easy to implement your own one. New
handlers will be detected automatically and will be available after a restart of Swift. There a three requirements
for a handler to be correctly recognized:

1. The new python module must be in the same folder as all other source code files of this package (which is in lib -> site-packages -> SwiftCam -> webcam_utils in your python environment)
2. The filename of the new module must end with `_supply.py`
3. The new module must implement a class whose name ends with `_camera`

The easiest way is to start from the random example camera `random_example_supply.py` and alter it. As you can see there,
the camera is immediately started when an instance of the camera class is created. The `__init__` method has to take the
url as a first argument and accept the keyword arguments `user`, `password` and `max_framerate`.
Passing images is done by a buffer class of which the camera has to hold an instance under the attribute `buffer`. The
easiest way is to use the buffer code shipped with this package. Images in the buffer have to be either numpy arrays
or PIL Image objects. They can be sent to the buffer by calling `buffer.put(image)`.
The camera class also has to implement a method `close` which should take care of stopping the loop that puts images
into the buffer.
The "format" tag assigned to your new camera handler will be the part of the camera class name before the first
underscore. For example if your handler implements the class `my_new_camera`, the format of this camera will be
"my". This naming is case-insensitive.

¹www.nion.com/swift

²https://github.com/mikeboers/PyAV

³https://github.com/Brow71189/PyAmScope