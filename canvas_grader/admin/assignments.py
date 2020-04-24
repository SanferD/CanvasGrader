from django.contrib import admin
from canvas_grader.models import Assignment, Quiz, QuizQuestionGroup, QuizQuestion
from canvas_grader.admin import model_admins as cga

@admin.register(Assignment)
class AssignmentAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(Quiz)
class QuizAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(QuizQuestionGroup)
class QuizQuestionGroupAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(QuizQuestion)
class QuizQuestionAdmin(cga.ROModelAdmin):
    inlines = []

