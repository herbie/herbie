import json
from django.contrib import admin
from django.utils.safestring import mark_safe

from wayneapp.models import AbstractBusinessEntity
from wayne import settings
from wayneapp.services import BusinessEntityManager


if not settings.WAYNE_ADMIN.get('DELETE_ENABLED'):
    admin.site.disable_action('delete_selected')


class ReadOnlyAdmin(admin.ModelAdmin):
    fields = ('key', 'version', 'data_prettified', 'created', 'modified')
    list_display = ['key', 'version']
    search_fields = ['key', 'version']

    _entity_manager = BusinessEntityManager()

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return settings.WAYNE_ADMIN.get('DELETE_ENABLED')

    def delete_model(self, request, entity):
        self._entity_manager.delete_by_instance(entity)

    def delete_queryset(self, request, queryset):
        self._entity_manager.delete_by_queryset(queryset)

    def data_prettified(self, model):
        json_data = json.dumps(model.data, sort_keys=True, indent=2)
        return mark_safe('<pre id="json-renderer" class="json-document">' + json_data + '</pre>')

    data_prettified.short_description = 'data'

    class Media:
        js = (settings.JSON_VIEWER.get('JS_URL'), settings.WAYNE_ADMIN.get('JS_URL'))
        css = {
            'all': (settings.JSON_VIEWER.get('CSS_URL'), settings.WAYNE_ADMIN.get('CSS_URL'))
        }


admin.site.register([cls for cls in AbstractBusinessEntity.__subclasses__()], ReadOnlyAdmin)
