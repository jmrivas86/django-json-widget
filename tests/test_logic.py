#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-json-widget
------------

Tests for `django-json-widget` widgets module.
"""

import json

from django.forms import Form, CharField
from django.test import TestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorWidgetInitializationTests(TestCase):
    """Test widget initialization and configuration"""

    def test_default_initialization(self):
        """Test widget with default parameters"""
        widget = JSONEditorWidget()

        expected_options = {
            "modes": ["text", "code", "tree", "form", "view"],
            "mode": "code",
            "search": True,
        }

        self.assertEqual(widget.options, expected_options)
        self.assertIsNone(widget.width)
        self.assertIsNone(widget.height)

    def test_custom_mode_initialization(self):
        """Test widget with custom mode"""
        widget = JSONEditorWidget(mode="tree")

        self.assertEqual(widget.options["mode"], "tree")

    def test_custom_options_initialization(self):
        """Test widget with custom options"""
        custom_options = {
            "mode": "form",
            "search": False,
            "statusBar": False,
        }
        widget = JSONEditorWidget(options=custom_options)

        # Should merge with defaults
        expected_options = {
            "modes": ["text", "code", "tree", "form", "view"],
            "mode": "form",  # overridden
            "search": False,  # overridden
            "statusBar": False,  # added
        }

        self.assertEqual(widget.options, expected_options)

    def test_width_height_initialization(self):
        """Test widget with custom width and height"""
        widget = JSONEditorWidget(width="100%", height="600px")

        self.assertEqual(widget.width, "100%")
        self.assertEqual(widget.height, "600px")

    def test_attrs_initialization(self):
        """Test widget with custom attributes"""
        attrs = {"class": "custom-json-editor", "data-test": "value"}
        widget = JSONEditorWidget(attrs=attrs)

        self.assertEqual(widget.attrs, attrs)

    def test_options_override_precedence(self):
        """Test that custom options properly override defaults"""
        custom_options = {
            "modes": ["code", "text"],  # Override default modes
            "mode": "text",  # Override default mode
            "search": False,  # Override default search
        }
        widget = JSONEditorWidget(options=custom_options)

        self.assertEqual(widget.options["modes"], ["code", "text"])
        self.assertEqual(widget.options["mode"], "text")
        self.assertFalse(widget.options["search"])


class JSONEditorWidgetContextTests(TestCase):
    """Test widget context generation"""

    def test_get_context_basic(self):
        """Test basic context generation"""
        widget = JSONEditorWidget()
        context = widget.get_context(
            "test_field", '{"key": "value"}', {"id": "test_id"}
        )
        self.assertIn("widget", context)
        self.assertEqual(context["widget"]["name"], "test_field")
        self.assertEqual(context["widget"]["value"], {"key": "value"})
        self.assertIn("options", context["widget"])
        self.assertIsNone(context["widget"]["width"])
        self.assertIsNone(context["widget"]["height"])

    def test_get_context_with_dimensions(self):
        """Test context generation with width and height"""
        widget = JSONEditorWidget(width="800px", height="400px")
        context = widget.get_context("test_field", "{}", {"id": "test_id"})

        self.assertEqual(context["widget"]["width"], "800px")
        self.assertEqual(context["widget"]["height"], "400px")
        self.assertIn("options", context["widget"])

    def test_get_context_options_serialization(self):
        """Test that options are properly JSON serialized in context"""
        custom_options = {
            "mode": "tree",
            "search": False,
            "navigationBar": True,
        }
        widget = JSONEditorWidget(options=custom_options)
        context = widget.get_context("test_field", "{}", {"id": "test_id"})

        # Options should be JSON serialized
        options_json = context["widget"]["options"]
        self.assertIsInstance(options_json, str)

        # Should be valid JSON
        parsed_options = json.loads(options_json)
        self.assertEqual(parsed_options["mode"], "tree")
        self.assertFalse(parsed_options["search"])
        self.assertTrue(parsed_options["navigationBar"])


class JSONEditorWidgetValueFormattingTests(TestCase):
    """Test widget value formatting"""

    def test_format_value_valid_json_string(self):
        """Test formatting valid JSON string"""
        widget = JSONEditorWidget()

        json_string = '{"name": "John", "age": 30}'
        result = widget.format_value(json_string)

        expected = {"name": "John", "age": 30}
        self.assertEqual(result, expected)

    def test_format_value_invalid_json(self):
        """Test formatting invalid JSON string raises error"""
        widget = JSONEditorWidget()

        invalid_json = '{"invalid": json}'

        with self.assertRaises(json.JSONDecodeError):
            widget.format_value(invalid_json)

    def test_format_value_none_or_empty(self):
        """Test formatting None value"""
        widget = JSONEditorWidget()

        with self.assertRaises((TypeError, json.JSONDecodeError)):
            widget.format_value(None)
        with self.assertRaises((TypeError, json.JSONDecodeError)):
            widget.format_value(None)


class JSONEditorWidgetTemplateRenderingTests(TestCase):
    """Test widget template rendering"""

    def test_template_name(self):
        """Test correct template name is set"""
        widget = JSONEditorWidget()
        self.assertEqual(widget.template_name, "django_json_widget.html")

    def test_template_exists(self):
        """Test that template exists"""
        from os import getcwd, path
        widget = JSONEditorWidget()
        template_file = path.join(getcwd(), "django_json_widget", "templates", widget.template_name)
        self.assertTrue(str(template_file).endswith("django_json_widget.html"))
        self.assertTrue(path.exists(template_file))

    def test_render_basic(self):
        """Test basic widget rendering"""
        widget = JSONEditorWidget()
        html = widget.render("test_field", '{"test": "value"}', {"id": "id_test_field"})

        # Check for essential elements
        self.assertIn("id_test_field", html)
        self.assertIn("test_field", html)
        self.assertIn("JSONEditor", html)
        self.assertIn("textarea", html)

    def test_render_with_custom_dimensions(self):
        """Test rendering with custom width and height"""
        widget = JSONEditorWidget(width="100%", height="300px")
        html = widget.render("test_field", "{}", {"id": "id_test_field"})

        self.assertIn("width:100%", html)
        self.assertIn("height:300px", html)

    def test_render_with_custom_attrs(self):
        """Test rendering with custom attributes"""
        widget = JSONEditorWidget()
        attrs = {"class": "custom-class", "data-test": "value"}
        html = widget.render("test_field", "{}", attrs)

        self.assertIn("custom-class", html)
        self.assertIn('data-test="value"', html)

    def test_render_javascript_options(self):
        """Test that JavaScript options are properly rendered"""
        custom_options = {"mode": "tree", "search": False}
        widget = JSONEditorWidget(options=custom_options)
        html = widget.render("test_field", "{}", {"id": "id_test_field"})

        # Should contain the serialized options
        self.assertIn('"mode": "tree"', html)
        self.assertIn('"search": false', html)


class JSONEditorWidgetFormIntegrationTests(TestCase):
    """Test widget integration with Django forms"""

    def test_form_field_integration(self):
        """Test widget works with form fields"""

        class TestForm(Form):
            json_data = CharField(widget=JSONEditorWidget())

        form = TestForm()
        self.assertIsInstance(form.fields["json_data"].widget, JSONEditorWidget)

    def test_form_field_with_initial_data(self):
        """Test form field with initial JSON data"""

        class TestForm(Form):
            json_data = CharField(
                widget=JSONEditorWidget(mode="tree"),
                initial='{"name": "test", "value": 123}',
            )

        form = TestForm()
        html = str(form["json_data"])

        self.assertIn("json_data", html)
        self.assertIn('"mode": "tree"', html)

    def test_form_validation_with_widget(self):
        """Test form validation with widget"""

        class TestForm(Form):
            json_data = CharField(widget=JSONEditorWidget(), required=True)

        # Test valid data
        form = TestForm({"json_data": '{"valid": "json"}'})
        self.assertTrue(form.is_valid())

        # Test empty data
        form = TestForm({"json_data": ""})
        self.assertFalse(form.is_valid())

    def test_form_media_inclusion(self):
        """Test that form includes widget media"""

        class TestForm(Form):
            json_data = CharField(widget=JSONEditorWidget())

        form = TestForm()
        media = form.media

        self.assertIn("dist/jsoneditor.min.js", str(media))
        self.assertIn("dist/jsoneditor.min.css", str(media))


class JSONEditorWidgetEdgeCasesTests(TestCase):
    """Test edge cases and error conditions"""

    def test_unicode_json_handling(self):
        """Test widget handles Unicode JSON properly"""
        widget = JSONEditorWidget()
        unicode_json = '{"name": "José", "city": "São Paulo", "emoji": "🎉"}'

        result = widget.format_value(unicode_json)
        self.assertEqual(result["name"], "José")
        self.assertEqual(result["city"], "São Paulo")
        self.assertEqual(result["emoji"], "🎉")


class JSONEditorWidgetAccessibilityTests(TestCase):
    """Test widget accessibility features"""

    def test_textarea_for_screen_readers(self):
        """Test that widget includes hidden textarea for accessibility"""
        widget = JSONEditorWidget()
        html = widget.render("test_field", "{}", {"id": "id_test_field"})

        # Should have hidden textarea for form submission and screen readers
        self.assertIn("textarea", html)
        self.assertIn("id_test_field_textarea", html)
        self.assertIn('style="display: none"', html)

    def test_proper_field_naming(self):
        """Test that widget generates proper field names"""
        widget = JSONEditorWidget()
        html = widget.render("json_field", "{}", {"id": "id_json_field"})

        self.assertIn('name="json_field"', html)
        self.assertIn('id="id_json_field"', html)
