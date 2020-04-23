from canvas_grader import api
from canvas_grader.models import Course, CourseLink
from django.utils.dateparse import parse_datetime

def Populate(token):
    api_courses = api.GetCourses(token)
    for api_course in api_courses:
        c = api_course.attributes
        created_at = parse_datetime(  c["created_at"]  )
        course, _ = Course.objects.get_or_create(
                    course_id = c["id"],
                    domain = token.domain,
                    defaults = {
                        "name": c["name"],
                        "created_at": created_at,
                    })
        course_link = CourseLink.objects.get_or_create(
                        user = token.user,
                        course = course)

