#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_jsoneditor_access
----------------------

Tests for JsonEditor instance accessibility from external JavaScript.
"""

from django.template import Context, Template
from django.test import TestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorAccessTests(TestCase):
    """Test JsonEditor instance accessibility"""

    def test_template_exposes_editor_to_window(self):
        """Test that JsonEditor instance is exposed to window object"""
        widget = JSONEditorWidget()
        context = widget.get_context("test_field", '{"key": "value"}', {"id": "test_id"})

        # Render the template
        template = Template('{% load static %}{% include "django_json_widget.html" %}')
        rendered = template.render(Context({"widget": context["widget"]}))

        # Check that the window assignment code is present
        self.assertIn("window['test_id_editor'] = editor", rendered)

    def test_template_exposes_editor_to_dom(self):
        """Test that JsonEditor instance is attached to DOM container"""
        widget = JSONEditorWidget()
        context = widget.get_context("test_field", '{"key": "value"}', {"id": "test_id"})

        # Render the template
        template = Template('{% load static %}{% include "django_json_widget.html" %}')
        rendered = template.render(Context({"widget": context["widget"]}))

        # Check that the DOM assignment code is present
        self.assertIn("container.jsonEditor = editor", rendered)

    def test_multiple_widgets_different_ids(self):
        """Test that multiple widgets get different window object names"""
        widget1 = JSONEditorWidget()
        widget2 = JSONEditorWidget()

        context1 = widget1.get_context("field1", "{}", {"id": "id_field1"})
        context2 = widget2.get_context("field2", "{}", {"id": "id_field2"})

        template = Template('{% load static %}{% include "django_json_widget.html" %}')

        rendered1 = template.render(Context({"widget": context1["widget"]}))
        rendered2 = template.render(Context({"widget": context2["widget"]}))

        # Each widget should have its own unique window object name
        self.assertIn("window['id_field1_editor'] = editor", rendered1)
        self.assertIn("window['id_field2_editor'] = editor", rendered2)
        self.assertNotEqual(rendered1, rendered2)
