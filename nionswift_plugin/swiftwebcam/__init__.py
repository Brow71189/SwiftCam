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

import gettext
import typing

from nion.ui import Declarative
from nion.utils import Converter
from nion.utils import Model
from nion.utils import Registry

from webcam_utils import webcam


_ = gettext.gettext


class VideoDeviceFactory:

    display_name = _("Swift Cam")
    factory_id = "swiftcam"

    def make_video_device(self, settings: dict) -> typing.Optional[webcam.Camera]:
        if settings.get("driver") == self.factory_id:
            camera_id = settings.get("device_id", settings.get("id"))
            camera_name = settings.get("name")
            try:
                video_device = webcam.Camera(**settings)
                video_device.camera_id = camera_id
                video_device.camera_name = camera_name
                return video_device
            except Exception as detail:
                print('Could not register camera {:s}. Reason: {:s}'.format(camera_id, str(detail)))
        return None

    def describe_settings(self) -> typing.List[typing.Dict]:
        return [
            {'name': 'camera_index', 'type': 'int'},
            {'name': 'url', 'type': 'string'},
            {'name': 'format', 'type': 'string'},
            {'name': 'user', 'type': 'string'},
            {'name': 'password', 'type': 'string'},
            {'name': 'max_framerate', 'type': 'int'}
        ]

    def get_editor_description(self):
        u = Declarative.DeclarativeUI()

        format_combo = u.create_combo_box(items=["acti_tcm4201", "mjpeg", "pyav", "random"], current_index="@binding(format_index_model.value)")
        url_field = u.create_line_edit(text="@binding(settings.url)", width=360)
        user_field = u.create_line_edit(text="@binding(settings.user)", width=200)
        password_field = u.create_line_edit(text="@binding(settings.password)", width=200)
        max_framerate_field = u.create_line_edit(text="@binding(settings.max_framerate, converter=int_converter)", width=200)

        label_column = u.create_column(u.create_label(text=_("Format:")), u.create_label(text=_("URL:")), u.create_label(text=_("User (optional):")), u.create_label(text=_("Password (optional):")), u.create_label(text=_("Max. Framerate (0 for none):")), spacing=4)
        field_column = u.create_column(format_combo, url_field, user_field, password_field, max_framerate_field, spacing=4)

        return u.create_row(label_column, field_column, u.create_stretch(), spacing=12)

    def create_editor_handler(self, settings):

        class EditorHandler:

            def __init__(self, settings):
                self.settings = settings

                self.format_index_model = Model.PropertyModel()

                formats = ["acti_tcm4201", "mjpeg", "pyav", "random"]

                def format_index_changed(index):
                    self.settings.format = formats[index]

                self.format_index_model.on_value_changed = format_index_changed

                self.int_converter = Converter.IntegerToStringConverter()

                self.format_index_model.value = formats.index(self.settings.format) if self.settings.format in formats else 2

        return EditorHandler(settings)


class WebcamExtension:

    extension_id = "nion.webcam"

    def __init__(self, api_broker):
        self.api = api_broker.get_api(version='~1.0', ui_version='~1.0')
        Registry.register_component(VideoDeviceFactory(), {"video_device_factory"})

    def close(self):
        pass
