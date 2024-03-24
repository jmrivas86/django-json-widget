from django.contrib import admin
from django.db.models import JSONField
from .models import Character
from django_json_widget.widgets import JSONEditorWidget


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
