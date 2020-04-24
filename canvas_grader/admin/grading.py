from django.contrib import admin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin
from canvas_grader.models import GradingView, GradingGroup, GroupQuestionLink
from canvas_grader.admin import model_admins as cga

class GradingGroupInline(cga.ROModelInline):
    model = GradingGroup
    inline_actions = []
    extra = 0

@admin.register(GradingView)
class GradingViewAdmin(cga.ROModelAdmin):
    inlines = [GradingGroupInline]

@admin.register(GradingGroup)
class GradingGroupAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(GroupQuestionLink)
class GroupQuestionLinkAdmin(cga.ROModelAdmin):
    inlines = []

