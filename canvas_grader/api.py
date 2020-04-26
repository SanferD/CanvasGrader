import os
from canvasapi import Canvas
import json
import logging, sys

DEBUG = False
if DEBUG:
    logger = logging.getLogger("canvasapi")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def GetCurrentUser(domain, token):
    return GetUserByUserId(domain, token, "self")

def GetUserByUserId(domain, token, user_id):
    canvas = GetCanvas(domain, token)
    user = canvas.get_user(user_id)
    return user

def GetCourse(token, course_id):
    canvas = GetCanvas(token.domain.url, token.token)
    course = canvas.get_course(course_id)
    return course

def GetCourses(token):
    canvas = GetCanvas(token.domain.url, token.token)
    courses = canvas.get_courses()
    ta_courses = [c for c in courses if IsTaCourse(c)]
    return ta_courses

def IsTaCourse(course):
    return course.attributes["enrollments"][0]["role"] in ("TaEnrollment", "TeacherEnrollment")

def GetQuizAssignments(course):
    assignments = GetAssignments(course)
    quiz_assignments = [a for a in assignments if a.attributes["is_quiz_assignment"]]
    return quiz_assignments

def GetAssignments(course):
    return course.get_assignments()

def GetCanvas(domain, token):
    domain = GetDomain(domain)
    canvas = Canvas(domain, token)
    return canvas

def GetDomain(domain):
    if not domain.startswith("https://"):
        domain = "https://" + domain
    domain = os.path.join(domain, "api", "v1") + "/"
    return domain

