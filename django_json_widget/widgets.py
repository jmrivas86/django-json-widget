import html
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

        if value:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass

            def escape_html_in_json(obj):
                if isinstance(obj, str):
                    return html.escape(obj)
                elif isinstance(obj, dict):
                    return {k: escape_html_in_json(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [escape_html_in_json(item) for item in obj]
                return obj

            # Escape HTML in the value
            safe_value = escape_html_in_json(value)
            # Convert back to JSON string
            context["widget"]["value"] = json.dumps(safe_value)

        return context

    def format_value(self, value):
        """
        When form is submitted, unescape the HTML entities in the JSON data
        """
        value = json.loads(value)
        if value:
            try:
                json_value = json.loads(value)

                def unescape_html_in_json(obj):
                    if isinstance(obj, str):
                        return html.unescape(obj)
                    elif isinstance(obj, dict):
                        return {k: unescape_html_in_json(v) for k, v in obj.items()}
                    elif isinstance(obj, (list, tuple)):
                        return [unescape_html_in_json(item) for item in obj]
                    return obj

                unescaped_value = unescape_html_in_json(json_value)
                return json.dumps(unescaped_value)
            except json.JSONDecodeError:
                return value
        return value
