from canvas_grader import api
from canvas_grader.models import Token, Course, CourseLink, \
                                 Assignment, Quiz, \
                                 QuizQuestionGroup, QuizQuestion
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
        course_link, _ = CourseLink.objects.get_or_create(
                        user = token.user,
                        course = course)
        PopulateWithAPICourse(course, api_course)

def PopulateCourseLink(course_link):
        course = course_link.course
        user = course_link.user
        token = Token.objects.get(user = user, domain = course.domain)
        api_course = api.GetCourse(token, course.course_id)
        PopulateWithAPICourse(course, api_course)

def PopulateWithAPICourse(course, api_course):
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
            PopulateWithAPIQuiz(quiz, api_quiz)

def PopulateWithAPIQuiz(quiz, api_quiz):
    api_questions = api_quiz.get_questions()
    for api_question in api_questions:
        a = api_question.attributes
        group_id = a["quiz_group_id"]
        if group_id:
            quiz_question_group, _ = QuizQuestionGroup.objects.get_or_create(
                                    quiz = quiz, group_id = group_id)
        else:
            quiz_question_group = None
        quiz_question, _ = QuizQuestion.UpdateOrCreate(
                                a["question_type"],
                                quiz = quiz,
                                question_id = a["id"],
                                defaults = {
                                    "question_name": a["question_name"],
                                    "question_text": a["question_text"],
                                    "quiz_question_group": quiz_question_group,
                                    "question_type": a["question_type"],
                                    "points_possible": a["points_possible"],
                                })

