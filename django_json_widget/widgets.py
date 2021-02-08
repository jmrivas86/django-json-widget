import json
from builtins import super

from django import forms
from django.conf import settings


class JSONEditorWidget(forms.Widget):
    class Media:
        js = (
            getattr(settings, "JSON_EDITOR_JS", 'dist/jsoneditor.min.js'),
        )
        css = {
            'all': (
                getattr(settings, "JSON_EDITOR_CSS", 'dist/jsoneditor.min.css'),
            )
        }

    template_name = 'django_json_widget.html'

    def __init__(self, attrs=None, mode='code', options=None, width=None, height=None):
        default_options = {
            'modes': ['text', 'code', 'tree', 'form', 'view'],
            'mode': mode,
            'search': True,
        }
        if options:
            default_options.update(options)

        self.options = default_options
        self.width = width
        self.height = height

        super(JSONEditorWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['options'] = json.dumps(self.options)
        context['widget']['width'] = self.width
        context['widget']['height'] = self.height

        return context
