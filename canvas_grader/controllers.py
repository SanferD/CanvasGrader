from canvas_grader import api
from canvas_grader.models import Course, CourseLink, Assignment, Quiz
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

        api_quiz_assignments = api.GetQuizAssignments(api_course)
        for api_quiz_assignment in api_quiz_assignments:
            a = api_quiz_assignment.attributes
            created_at = parse_datetime(  a["created_at"]  )
            updated_at = parse_datetime(  a["updated_at"]  )
            points_possible = a["points_possible"] if a["points_possible"] else 0.0
            assignment, _ = Assignment.objects.get_or_create(
                                    course = course,
                                    assignment_id = a["id"],
                                    defaults = {
                                        "name": a["name"],
                                        "points_possible": points_possible,
                                        "created_at": created_at,
                                        "updated_at": updated_at,
                                        "html_url": a["html_url"],
                                    })

            api_quiz = api_course.get_quiz(a["quiz_id"])
            q = api_quiz.attributes
            quiz, _ = Quiz.objects.get_or_create(
                        assignment = assignment,
                        quiz_id = q["id"],
                        defaults = {
                            "speed_grader_url": q["speed_grader_url"],
                            "question_count": q["question_count"],
                        })


