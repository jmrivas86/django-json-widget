from unittest import skipUnless

from django.apps import apps
from django.db import models
from django.test import SimpleTestCase
from django.test.utils import isolate_apps

from django_json_widget.widgets import JSONEditorWidget


@skipUnless(apps.is_installed('wagtail'), 'Requires tests.wagtail_settings')
class WagtailPanelTests(SimpleTestCase):
    @isolate_apps('tests')
    def test_inline_panel_includes_widget_and_empty_form_template(self):
        from modelcluster.fields import ParentalKey
        from modelcluster.models import ClusterableModel
        from wagtail.admin.panels import FieldPanel, InlinePanel, ObjectList

        class Parent(ClusterableModel):
            class Meta:
                app_label = 'tests'

        class Child(models.Model):
            parent = ParentalKey(Parent, related_name='items', on_delete=models.CASCADE)
            data = models.JSONField(blank=True, null=True)

            class Meta:
                app_label = 'tests'

        panel = ObjectList([
            InlinePanel('items', panels=[FieldPanel('data', widget=JSONEditorWidget())]),
        ]).bind_to_model(Parent)
        instance = Parent()
        instance.items.add(Child(data={'saved': True}))
        form = panel.get_form_class()(instance=instance)
        html = panel.get_bound_panel(instance=instance, form=form).render_html()
        self.assertIn('id_items-0-data', html)
        self.assertIn('id_items-__prefix__-data', html)
        self.assertIn('data-jsoneditor-options=', html)
        self.assertIn('django_json_widget.js', form.media._js)

    @isolate_apps('tests')
    def test_field_panel_renders_widget_media_and_validates_submissions(self):
        from wagtail.admin.panels import FieldPanel, ObjectList

        class Record(models.Model):
            data = models.JSONField(blank=True, null=True)

            class Meta:
                app_label = 'tests'

        panel = ObjectList([
            FieldPanel('data', widget=JSONEditorWidget()),
        ]).bind_to_model(Record)
        form_class = panel.get_form_class()
        instance = Record(data={'saved': True})
        form = form_class(instance=instance)
        html = panel.get_bound_panel(instance=instance, form=form).render_html()
        self.assertIn('data-jsoneditor-options=', html)
        self.assertIn('"saved": true', html)
        self.assertEqual(form.media._js, ['dist/jsoneditor.min.js', 'django_json_widget.js'])

        updated = form_class({'data': '{"new":true}'}, instance=instance)
        self.assertTrue(updated.is_valid(), updated.errors)
        self.assertEqual(updated.save(commit=False).data, {'new': True})

        invalid = form_class({'data': '{'}, instance=instance)
        self.assertFalse(invalid.is_valid())
        self.assertIn('data-jsoneditor-invalid="true"', str(invalid['data']))

        cleared = form_class({'data': ''}, instance=instance)
        self.assertTrue(cleared.is_valid(), cleared.errors)
        self.assertIsNone(cleared.save(commit=False).data)
