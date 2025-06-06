import json

from django.test import TestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorWidgetTest(TestCase):
    def setUp(self):
        self.widget = JSONEditorWidget(width=100, height=50)

    def test_init(self):
        self.assertEqual(self.widget.width, 100)
        self.assertEqual(self.widget.height, 50)

    def test_format_value_none(self):
        self.assertIsNone(self.widget.format_value(None))

    def test_format_value_empty_string(self):
        self.assertEqual(self.widget.format_value(""), "")

    def test_format_value_json_str(self):
        data = {
            "key": "value",
            "str": "&lt;a&gt;",
            "dict": {
                "str": "&lt;a&gt;",
            },
            "list": ["&lt;a&gt;"],
        }
        self.assertEqual(
            json.loads(self.widget.format_value(json.dumps(data))),
            {
                "key": "value",
                "str": "<a>",
                "dict": {
                    "str": "<a>",
                },
                "list": ["<a>"],
            },
        )

    def test_format_value_dict(self):
        self.assertEqual(
            self.widget.format_value({"key": "value"}),
            '{"key": "value"}'
        )
