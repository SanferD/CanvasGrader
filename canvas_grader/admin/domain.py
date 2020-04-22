from django.contrib import admin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin
from canvas_grader.models import Domain

@admin.register(Domain)
class DomainAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    inlines = []

    def has_add_permission(self, request, obj = None):
        return False

