from django.contrib import admin
from django.db.models import JSONField
from .models import Character, CharacterDetail
from django_json_widget.widgets import JSONEditorWidget


class CharacterDetailInline(admin.TabularInline):
    model = CharacterDetail
    extra = 0
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget(height='350px', width='700px')},
    }


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    inlines = [CharacterDetailInline]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
