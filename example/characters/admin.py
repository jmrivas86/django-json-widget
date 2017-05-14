from django.contrib import admin
from django.contrib.postgres import fields
from .models import Character
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
