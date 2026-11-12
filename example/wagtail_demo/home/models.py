from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey

from django_json_widget.widgets import JSONEditorWidget


class HomePage(Page):
    settings_json = models.JSONField(default=dict, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("settings_json", widget=JSONEditorWidget()),
        InlinePanel("json_items", label="JSON items"),
    ]


class JSONItem(models.Model):
    page = ParentalKey(HomePage, related_name="json_items", on_delete=models.CASCADE)
    data = models.JSONField(default=dict, blank=True)

    panels = [FieldPanel("data", widget=JSONEditorWidget())]
