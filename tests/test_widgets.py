from django.test import TestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorWidgetTest(TestCase):
    def setUp(self):
        self.widget = JSONEditorWidget(width=100, height=50)

    def test_init(self):
        self.assertEqual(self.widget.width, 100)
        self.assertEqual(self.widget.height, 50)

    def test_format_value_json_str(self):
        self.assertEqual(self.widget.format_value('{"test":1}'), {"test": 1})

    def test_format_value_dict(self):
        self.assertEqual(self.widget.format_value({"key": "value"}), {"key": "value"})
