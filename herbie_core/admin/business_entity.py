import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings

from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.business_entity_manager import BusinessEntityManager


class ReadOnlyAdmin(admin.ModelAdmin):
    fields = ("key", "version", "data_prettified", "created", "modified")
    list_display = ["key", "version"]
    search_fields = ["key", "version"]

    _entity_manager = BusinessEntityManager()

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            return True

        return request.user.has_perm("herbie_core.view_business_entities")

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def delete_model(self, request, entity):
        self._entity_manager.delete_by_instance(entity)

    def delete_queryset(self, request, queryset):
        self._entity_manager.delete_by_queryset(queryset)

    def data_prettified(self, model):
        json_data = json.dumps(model.data, sort_keys=True, indent=2)
        return mark_safe('<pre id="json-renderer" class="json-document">' + json_data + "</pre>")

    data_prettified.short_description = "data"

    class Media:
        js = (settings.JSON_VIEWER.get("JS_URL"), settings.HERBIE_ADMIN.get("JS_URL"))
        css = {"all": (settings.JSON_VIEWER.get("CSS_URL"), settings.HERBIE_ADMIN.get("CSS_URL"))}


admin.site.register([cls for cls in AbstractBusinessEntity.__subclasses__()], ReadOnlyAdmin)
