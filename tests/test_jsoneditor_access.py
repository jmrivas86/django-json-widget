from unittest.mock import patch

from django.test import SimpleTestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorAccessTests(SimpleTestCase):
    def test_missing_style_renders_dimensions_without_template_debug_log(self):
        with patch('django.template.base.logger.debug') as debug:
            html = JSONEditorWidget(width='600px').render('data', '{}', {'id': 'id_data'})
        debug.assert_not_called()
        self.assertIn('style="height:500px;width:600px;display:inline-block;"', html)

    def test_custom_style_overrides_default_dimensions(self):
        html = JSONEditorWidget(width='600px').render(
            'data', '{}', {'id': 'id_data', 'style': 'width:42px'}
        )
        self.assertIn('style="width:42px"', html)
        self.assertNotIn('width:600px', html)

    def test_initializer_loaded_after_editor_library(self):
        scripts = JSONEditorWidget().media._js
        self.assertLess(scripts.index('dist/jsoneditor.min.js'), scripts.index('django_json_widget.js'))

    def test_empty_value_renders_as_null(self):
        html = JSONEditorWidget().render('data', None, {'id': 'id_data'})
        self.assertIn('type="application/json">null</script>', html)

    def test_options_are_html_escaped(self):
        html = JSONEditorWidget(options={'name': '</div><script>alert(1)</script>'}).render(
            'data', '{}', {'id': 'id_data'}
        )
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_invalid_json_redisplays_with_validation_error(self):
        from django import forms

        class Form(forms.Form):
            data = forms.JSONField(widget=JSONEditorWidget())

        form = Form({'data': '{'})
        self.assertFalse(form.is_valid())
        html = str(form['data'])
        self.assertIn('data-jsoneditor-invalid="true"', html)
        self.assertIn('type="application/json">"{"</script>', html)
