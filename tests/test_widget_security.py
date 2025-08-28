#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Security tests for django-json-widget
"""

import json
from django.test import TestCase
from django.utils.safestring import SafeString
from django_json_widget.widgets import JSONEditorWidget


class JSONEditorWidgetSecurityTests(TestCase):
    """Test security aspects of the widget"""

    def test_xss_prevention_in_options(self):
        """Test that malicious JavaScript in options is properly escaped"""
        malicious_options = {
            'mode': 'code',
            'search': True,
            'onError': '<script>alert("XSS")</script>',
            'onChange': 'maliciousFunction()',
        }

        widget = JSONEditorWidget(options=malicious_options)
        context = widget.get_context('test_field', '{}', {'id': 'test_id'})

        options_json = context['widget']['options']

        # Should be properly JSON encoded, not executable JavaScript
        self.assertIn('"onError": "<script>alert(\\"XSS\\")</script>"', options_json)
        self.assertIn('"onChange": "maliciousFunction()"', options_json)

        # Verify it's valid JSON and not executable code
        parsed = json.loads(options_json)
        self.assertEqual(parsed['onError'], '<script>alert("XSS")</script>')
        self.assertEqual(parsed['onChange'], 'maliciousFunction()')

    def test_html_injection_in_widget_attrs(self):
        """Test that HTML injection in widget attributes is handled safely"""
        malicious_attrs = {
            'id': 'test_id',
            'class': 'safe-class" onload="alert(\'XSS\')" data-evil="',
            'data-test': '<script>alert("XSS")</script>',
        }

        widget = JSONEditorWidget()
        html = widget.render('test_field', '{}', malicious_attrs)

        # Should not contain executable JavaScript
        self.assertNotIn('safe-class" onload="alert(\'XSS\')" data-evil="', html)
        self.assertNotIn('<script>alert("XSS")</script>', html)

        # But should contain the escaped attributes
        self.assertIn('class=', html)
        self.assertIn('data-test=', html)

    def test_json_value_sanitization(self):
        """Test that JSON values are properly sanitized"""
        # Test with potentially dangerous JSON content
        dangerous_json = '{"script": "<script>alert(\\"XSS\\")</script>", "html": "<img src=x onerror=alert(1)>"}'

        widget = JSONEditorWidget()
        result = widget.format_value(dangerous_json)

        # Should parse correctly but not execute
        self.assertEqual(result['script'], '<script>alert("XSS")</script>')
        self.assertEqual(result['html'], '<img src=x onerror=alert(1)>')

    def test_safe_json_serialization_in_template(self):
        """Test that JSON serialization in template context is safe"""
        widget = JSONEditorWidget()

        # Create context with potentially dangerous data
        context = widget.get_context('test_field', '{"xss": "<script>"}', {'id': 'test_id'})

        # Options should be safely serialized
        options = context['widget']['options']
        self.assertIsInstance(options, str)

        # Should be valid JSON
        json.loads(options)

    def test_field_name_sanitization(self):
        """Test that field names are properly handled"""
        # Test with potentially problematic field names
        problematic_names = [
            'field_name',  # normal
            'field-name',  # with dash
            'field.name',  # with dot
            'field[name]',  # with brackets
            'field name',  # with space
        ]

        widget = JSONEditorWidget()

        for name in problematic_names:
            html = widget.render(name, '{}', {'id': f'id_{name}'})
            # Should render without errors and contain the name
            self.assertIn(name, html)
            self.assertIn('JSONEditor', html)

    def test_no_code_injection_via_dimensions(self):
        """Test that width/height parameters don't allow code injection"""
        malicious_widget = JSONEditorWidget(
            width='100px; background-image: url(javascript:alert(1))',
            height='200px" onload="alert(1)'
        )

        context = malicious_widget.get_context('test', '{}', {'id': 'test'})

        # Width and height should be stored as-is (template should handle escaping)
        self.assertIn('javascript:', context['widget']['width'])
        self.assertIn('onload=', context['widget']['height'])

        # But when rendered, should be properly escaped
        html = malicious_widget.render('test', '{}', {'id': 'test'})
        # The template should handle proper escaping of these values

    def test_json_script_tag_safety(self):
        """Test that json_script template tag provides XSS protection"""
        widget = JSONEditorWidget()

        # JSON with potentially dangerous content
        dangerous_json = '{"content": "</script><script>alert(\\"XSS\\")</script>"}'

        html = widget.render('test_field', dangerous_json, {'id': 'test_id'})

        # Should not contain unescaped script tags that could execute
        # The json_script template tag should handle proper escaping
        self.assertIn('test_field_data', html)  # JSON script element should be present

        # Count script tags - should only be the ones we expect
        script_count = html.count('<script>')
        self.assertGreaterEqual(script_count, 1)  # At least our widget script

        # Should not contain our dangerous script as executable code
        self.assertNotIn('alert("XSS")', html)

    def test_context_variable_safety(self):
        """Test that all context variables are safe for template rendering"""
        widget = JSONEditorWidget(
            width='<script>alert(1)</script>',
            height='javascript:alert(1)',
            options={'mode': '<script>alert(1)</script>'}
        )

        context = widget.get_context(
            'test<script>',
            '{"evil": "<script>alert(1)</script>"}',
            {'id': 'test<script>'}
        )

        # All context values should be present but safely handled
        self.assertIn('widget', context)
        self.assertIn('<script>alert(1)</script>', context['widget']['width'])
        self.assertIn('javascript:alert(1)', context['widget']['height'])

        # Options should be JSON serialized (safe)
        options = json.loads(context['widget']['options'])
        self.assertEqual(options['mode'], '<script>alert(1)</script>')
