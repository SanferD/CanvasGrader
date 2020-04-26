from canvas_grader import api
from canvas_grader.models import Token, Course, CourseLink, \
                                 Assignment, Quiz, \
                                 QuizQuestionGroup, QuizQuestion, \
                                 CanvasUser, Submission, \
                                 SubmissionHistoryItem, \
                                 SubmissionDatum, AssessmentItem
from django.utils.dateparse import parse_datetime
from canvasapi.quiz import QuizSubmission
from canvasapi.requester import Requester

def PopulateCoursesOnly(token):
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

def PopulateCourse(token, course):
    api_course = api.GetCourse(token, course.course_id)
    PopulateWithAPICourse(course, api_course)

def PopulateWithAPICourse(course, api_course):
    api_quiz_assignments = api.GetQuizAssignments(api_course)
    for api_quiz_assignment in api_quiz_assignments:
        PopulateQuizOnly(course, api_quiz_assignment)

def PopulateQuizOnly(course, api_course, api_quiz_assignment):
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

    api_quiz = api_course.get_quiz(api_quiz_assignment.attributes["quiz_id"])
    q = api_quiz.attributes
    quiz, _ = Quiz.objects.get_or_create(
                assignment = assignment,
                quiz_id = q["id"],
                defaults = {
                    "speed_grader_url": q["speed_grader_url"],
                    "question_count": q["question_count"],
                })
    PopulateWithAPIQuiz(quiz, api_quiz_assignment, api_quiz)

def PopulateQuiz(token, quiz):
    api_course = api.GetCourse(token, quiz.assignment.course.course_id)
    api_quiz_assignment = api_course.get_assignment(quiz.assignment.assignment_id)
    api_quiz = api_course.get_quiz(quiz.quiz_id)
    PopulateWithAPIQuiz(quiz, api_quiz_assignment, api_quiz)

def PopulateWithAPIQuiz(quiz, api_assignment, api_quiz):
    api_questions = api_quiz.get_questions()
    for api_question in api_questions:
        a = api_question.attributes
        group_id = a["quiz_group_id"]
        if group_id:
            quiz_question_group, _ = QuizQuestionGroup.objects.get_or_create(
                                    quiz = quiz, group_id = group_id)
        else:
            quiz_question_group = None
        quiz_question, _ = QuizQuestion.objects.get_or_create(
                                quiz = quiz,
                                question_id = a["id"],
                                defaults = {
                                    "question_name": a["question_name"],
                                    "question_text": a["question_text"],
                                    "quiz_question_group": quiz_question_group,
                                    "question_type": a["question_type"],
                                    "points_possible": a["points_possible"],
                                })
        api_submissions = api_assignment.get_submissions(include = ["submission_history", "user"])
        for api_submission in api_submissions:
            a = api_submission.attributes
            if a["workflow_state"] != "unsubmitted" and a["attempt"] is not None:
                api_user = a["user"]
                domain = quiz.assignment.course.domain
                canvas_user, _ = CanvasUser.objects.get_or_create(
                    user_id = api_user["id"],
                    domain = domain,
                    defaults = {
                        "name": api_user["name"],
                        "sortable_name": api_user["sortable_name"]
                })

                submission, _ = Submission.objects.get_or_create(
                                    submission_id = a["id"],
                                    assignment = quiz.assignment,
                                    defaults = {
                                        "posted_at": parse_datetime(a["posted_at"]),
                                        "preview_url": a["preview_url"],
                                        "canvas_user": canvas_user,
                                    })
                for api_sh in a["submission_history"]:
                    submission_history_item, _ = SubmissionHistoryItem.objects.get_or_create(
                        submission = submission,
                        submission_history_id = api_sh["id"])
                    
                    for d in api_sh["submission_data"]:
                        quiz_questions = QuizQuestion.objects.filter(
                                            quiz = quiz, question_id = d["question_id"])

                        if quiz_questions.count() > 0:
                            quiz_question = quiz_questions[0]
                            submission_datum, _ = SubmissionDatum.objects.get_or_create(
                                                    submission_history_item = submission_history_item,
                                                    quiz_question = quiz_question,
                                                    defaults = {
                                                        "text": d["text"],
                                                    })
                            if "more_comments" in d:
                                assessment_item, _ = AssessmentItem.objects.update_or_create(
                                                        submission_datum = submission_datum,
                                                        defaults = {
                                                            "score": d["points"],
                                                            "comment": d["more_comments"]
                                                        })

def UpdateScoreAndComments(token, assessment_item):
    domain = api.GetDomain(token.domain.url)
    requester = Requester(domain, token.token)
    sd = assessment_item.submission_datum
    shi = sd.submission_history_item
    quiz = Quiz.objects.get(assignment = shi.submission.assignment)
    attributes = {
        "course_id": quiz.assignment.course.course_id,
        "quiz_id": quiz.quiz_id,
        "id": shi.submission_history_id,
    }
    qs = QuizSubmission(requester, attributes)
    questions = {
        sd.quiz_question.question_id: {
            "score": assessment_item.score,
            "comment": assessment_item.comment,
        }
    }
    data = {
        "quiz_submissions": [{
            "attempt": 1,
            "questions": questions,
        }]
    }
    qs.update_score_and_comments(**data)

