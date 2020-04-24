from django.contrib import admin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin

class ROModelAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    def has_add_permission(self, request, obj = None):
        return False

    def has_change_permission(self, request, obj = None):
        return False

class ROModelInline(InlineActionsMixin, admin.TabularInline):
    def has_add_permission(self, request, obj = None):
        return False

    def has_change_permission(self, request, obj = None):
        return False
    

