from django.contrib import admin
from inline_actions.admin import InlineActionsMixin, InlineActionsModelAdminMixin
from canvas_grader.models import Domain, Course, CourseLink
from canvas_grader.admin import model_admins as cga

@admin.register(Domain)
class DomainAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(Course)
class CourseAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(CourseLink)
class CourseLinkAdmin(cga.ROModelAdmin):
    inlines = []

