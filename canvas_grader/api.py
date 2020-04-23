import os
from canvasapi import Canvas
import json

def GetCurrentUser(domain, token):
    return GetUserByUserId(domain, token, "self")

def GetUserByUserId(domain, token, user_id):
    canvas = GetCanvas(domain, token)
    user = canvas.get_user(user_id)
    return user

def GetCourses(token):
    canvas = GetCanvas(token.domain.url, token.token)
    courses = canvas.get_courses()
    ta_courses = [c for c in courses if IsTaCourse(c)]
    return ta_courses

def IsTaCourse(course):
    return course.attributes["enrollments"][0]["role"] in ("TaEnrollment", "TeacherEnrollment")

def GetCanvas(domain, token):
    if not domain.startswith("https://"):
        domain = "https://" + domain
    domain = os.path.join(domain, "api", "v1")
    canvas = Canvas(domain, token)
    return canvas

