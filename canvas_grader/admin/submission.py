from django.contrib import admin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin
from canvas_grader.models import CanvasUser, Submission, SubmissionHistoryItem, SubmissionDatum, AssessmentItem
from canvas_grader.admin import model_admins as cga

@admin.register(CanvasUser)
class CanvasUserAdmin(cga.ROModelAdmin):
    inlines = []

class SubmissionHistoryItemInline(cga.ROModelInline):
    model = SubmissionHistoryItem
    inline_actions = []
    extra = 0

@admin.register(Submission)
class SubmissionAdmin(cga.ROModelAdmin):
    inlines = [SubmissionHistoryItemInline]

class SubmissionDatumInline(cga.ROModelInline):
    model = SubmissionDatum
    inline_actions = []
    extra = 0

@admin.register(SubmissionHistoryItem)
class SubmissionHistoryItemAdmin(cga.ROModelAdmin):
    inlines = [SubmissionDatumInline]

class AssessmentItemInline(cga.ROModelInline):
    model = AssessmentItem
    inline_actions = []
    extra = 0

@admin.register(SubmissionDatum)
class SubmissionDatumAdmin(cga.ROModelAdmin):
    inlines = [AssessmentItemInline]

@admin.register(AssessmentItem)
class AssessmentItemAdmin(cga.ROModelAdmin):
    inlines = []

