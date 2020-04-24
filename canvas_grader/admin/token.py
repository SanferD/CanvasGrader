from django.contrib import admin
from canvas_grader.models import Profile, Token
from canvas_grader.admin import model_admins as cga

@admin.register(Profile)
class ProfileAdmin(cga.ROModelAdmin):
    inlines = []

@admin.register(Token)
class TokenAdmin(cga.ROModelAdmin):
    inlines = []

