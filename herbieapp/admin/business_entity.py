import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from herbieapp.models import AbstractBusinessEntity
from herbie import settings
from herbieapp.services import BusinessEntityManager


gdpr_delete_fields = ['email', 'person_email', 'person_gender', 'person_phone']
gdpr_anonname_fields = ['firstName', 'lastName', 'person_name', 'person_first_name', 'person_last_name']

def anonymize(modeladmin, request, queryset):
    for obj in queryset:
        for k in obj.data:
            if k in gdpr_delete_fields:
                obj.data[k] = None
            if k in gdpr_anonname_fields:
                obj.data[k] = 'Anonymous'
        obj.save()
anonymize.short_description = 'Delete all personal information'
anonymize.allowed_permissions = ('change',)


class ReadOnlyAdmin(admin.ModelAdmin):
    fields = ('key', 'version', 'data_prettified', 'created', 'modified')
    list_display = ['key', 'version']
    search_fields = ['key', 'version', 'data']
    actions = [anonymize]

    _entity_manager = BusinessEntityManager()

    def has_view_permission(self, request, obj=None):
        if super().has_view_permission(request, obj):
            return True

        return request.user.has_perm('herbieapp.view_business_entities')

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
        return mark_safe('<pre id="json-renderer" class="json-document">' + json_data + '</pre>')

    data_prettified.short_description = 'data'

    class Media:
        js = (settings.JSON_VIEWER.get('JS_URL'), settings.HERBIE_ADMIN.get('JS_URL'))
        css = {
            'all': (settings.JSON_VIEWER.get('CSS_URL'), settings.HERBIE_ADMIN.get('CSS_URL'))
        }


admin.site.register([cls for cls in AbstractBusinessEntity.__subclasses__()], ReadOnlyAdmin)
