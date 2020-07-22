import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings

from herbie_core.models.schema import Schema


class JsonSchemaAdmin(admin.ModelAdmin):
    fields = ("name", "version", "json_schema", "created", "modified")
    list_display = ["name", "version"]
    search_fields = ["name", "version"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def json_schema(self, model):
        json_data = json.dumps(model.content, sort_keys=True, indent=2)
        return mark_safe('<pre id="json-renderer" class="json-document">' + json_data + "</pre>")

    class Media:
        js = (settings.JSON_VIEWER.get("JS_URL"), settings.HERBIE_ADMIN.get("JS_URL"))
        css = {"all": (settings.JSON_VIEWER.get("CSS_URL"), settings.HERBIE_ADMIN.get("CSS_URL"))}


admin.site.register(Schema, JsonSchemaAdmin)
