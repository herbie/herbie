import json
from django.contrib import admin
from django.utils.safestring import mark_safe

from wayneapp.models import AbstractBusinessEntity
from wayne import settings

admin.site.disable_action('delete_selected')


class ReadOnlyAdmin(admin.ModelAdmin):
    fields = ('key', 'version', 'data_prettified', 'created', 'modified')
    list_display = ['key', 'version']
    search_fields = ['key', 'version']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

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
