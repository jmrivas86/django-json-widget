from django.test import TestCase

from django_json_widget.widgets import JSONEditorWidget


class JSONEditorWidgetTest(TestCase):
    def test_init(self):
        widget = JSONEditorWidget(width=100, height=50)
        self.assertEqual(widget.width, 100)
        self.assertEqual(widget.height, 50)
