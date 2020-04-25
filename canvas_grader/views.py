from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from canvas_grader.models import Domain, Token, Profile, Course, \
                                 CourseLink, Quiz, GradingView, \
                                 GradingGroup, GroupQuestionLink, \
                                 QuizQuestion, Submission, AssessmentItem
from canvas_grader import api
from canvas_grader import controllers

def Index(request):
    if request.user.is_authenticated:
        user = request.user
        tokens = Token.objects.filter(user = user)
        domains = [token.domain for token in tokens]
        response = render(request, "resources/domains.html", {"domains": domains})
    else:
        response = render(request, "login/login.html", {})
    return response

def Settings(request):
    return render(request, "tokens/tokens.html", {})

class Tokens(views.APIView):
    def get(self, request):
        user = request.user
        tokens = user.token_set.all()
        tokens = [t.serialize("domain") for t in tokens]
        return Response(tokens)

    def post(self, request):
        return self.__update(request, self.__createOrUpdateToken)

    def delete(self, request):
        return self.__update(request, self.__deleteToken)

    def __update(self, request, f):
        user = request.user
        if "tokens" in request.data:
            tokens = request.data["tokens"]
            for token in tokens:
                try:
                    f(user, token)
                except Exception:
                    pass
            response = Response(status = 200)
        else:
            response = Response(status = 400)
        return response

    def __createOrUpdateToken(self, user, data):
        id = data.get("id")
        api_token = data["token"]
        domain_url = data["domain"]
        # also a test for api call with domain + token pair
        u = api.GetCurrentUser(domain_url, api_token).attributes
        domain, _ = Domain.objects.get_or_create(url = domain_url)

        defaults = {"name": u["name"]}
        token = Token.objects.filter(id = id)
        if token:
            token.token = api_token
            token.domain = domain
            token.save()
        else:
            profile, _ = Profile.objects.get_or_create(
                            user_id = u["id"], defaults = defaults)
            token, _ = Token.objects.get_or_create(
                        user = user, token = api_token,
                        domain = domain, profile = profile)
        controllers.Populate(token)

    def __deleteToken(self, user, data):
        id = data.get("id")
        if id:
            Token.objects.get(id = id).delete()

def GetCourses(request, domain_id):
    user = request.user
    try:
        domain = Domain.objects.get(id = domain_id)
    except Domain.DoesNotExist:
        domain = None

    if domain:
        links = CourseLink.objects.filter(user = user)
        courses = [l.course for l in links]
    else:
        courses = None

    if domain is None or courses is None:
        response = Response(status = 404)
    else:
        data = {"domain": domain, "courses": courses}
        response = render(request, "resources/courses.html", data)
    return response

def GetQuizzes(request, course_id):
    user = request.user
    try:
        course = Course.objects.get(id = course_id)
    except Course.DoesNotExist:
        course = None

    if course:
        is_valid = CourseLink.objects.filter(user = user, course = course).count() != 0
    else:
        is_valid = False

    if is_valid:
        quizzes = Quiz.objects.filter(assignment__course = course)
        data = {"domain": course.domain, "course": course, "quizzes": quizzes}
        response = render(request, "resources/quizzes.html", data)
    else:
        response = Response(status = 404)
        
    return response

def AddGradingView(request, quiz_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        data = {"domain": course.domain, "course": course,
                "quiz": quiz, "grading_view": None}
        response = render(request, "grading/grading-view.html", data)
    else:
        response = Response(status = 404)
        
    return response

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def GetAllQuizQuestions(request, quiz_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        questions = [{"id": q.id, "name": q.question_name} for q in quiz.quizquestion_set.all()]
        response = Response(questions)
    else:
        response = Response(status = 404)
    return response

class GradingAPIViews(views.APIView):
    def get(self, request, quiz_id):
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            grading_views = GradingView.objects.filter(quiz = quiz)
            data = {"domain": course.domain, "course": course,
                    "quiz": quiz, "grading_views": grading_views}
            response = render(request, "resources/grading-views.html", data)
        else:
            response = Response(status = 404)
            
        return response

    def post(self, request, quiz_id):
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            data = request.data["grading_view"]
            grading_view, _ = GradingView.objects.get_or_create(
                                quiz = quiz, name = data["name"])
            for g in data["grading_groups"]:
                grading_group, _ = GradingGroup.objects.get_or_create(
                                    name = g["name"], grading_view = grading_view)
                for q in g["questions"]:
                    link, _ = GroupQuestionLink.objects.get_or_create(
                                    quiz_question = QuizQuestion.objects.get(id = q["id"]),
                                    grading_group = grading_group)
            response = Response(status = 200)
        else:
            response = Response(status = 404)
        return response
        
def GetGradingGroups(request, view_id):
    view, is_valid = ViewId2ViewValid(request, view_id)
    if is_valid:
        grading_groups = view.gradinggroup_set.all()
        quiz = view.quiz
        assignment = quiz.assignment
        course = assignment.course
        domain = course.domain
        data = {"domain": domain, "course": course, "quiz": quiz,
                "grading_view": view, "grading_groups": grading_groups}
        response = render(request, "resources/grading-groups.html", data)
    else:
        response = Response(status = 404)
    return response

def ViewId2ViewValid(request, view_id):
    user = request.user
    try:
        view = GradingView.objects.get(id = view_id)
    except GradingView.DoesNotExist:
        view = None

    quiz_id = view.quiz.id if view else None
    if quiz_id:
        _, _, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    else:
        is_valid = False
    return view, is_valid

def QuizId2CourseQuizValid(request, quiz_id):
    user = request.user
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        quiz = None

    if quiz:
        course = quiz.assignment.course
        is_valid = CourseLink.objects.filter(user = user, course = course).count() != 0
    else:
        course = None
        is_valid = False
    return course, quiz, is_valid

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def GetGradePageForQuiz(request, quiz_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        grading_group_id = request.GET["grading-group"]
        grading_group = GradingGroup.objects.filter(id = grading_group_id).first()
        if grading_group:
            questions = [l.quiz_question.serialize() for l in
                         grading_group.groupquestionlink_set.order_by("quiz_question__quiz_id")]
            for q in questions:
                can_answer = q["question_type"] != "text_only_question" 
                q["can_answer"] = can_answer
            print(questions)
            submissions = Submission.objects.filter(assignment__quiz = quiz)
            canvas_users = [s.canvas_user.serialize() for s in submissions]
            data = {"quiz": quiz, "questions": questions, "canvas_users": canvas_users}
            response = render(request, "grader/grader.html", data)
        else:
            response = Response(status = 404)
    else:
        response = Response(status = 404)
    return response

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def GetSubmission(request, quiz_id):
    canvas_user_id = request.GET.get("canvas-user", None)
    if canvas_user_id:
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            submission = Submission.objects.filter(
                            assignment = quiz.assignment,
                            canvas_user__id = canvas_user_id).first()
            if submission:
                shi = submission.submissionhistoryitem_set.first()
                submission_data = shi.submissiondatum_set.all()
                assessment_items = dict()
                for a in AssessmentItem.objects.filter(submission_datum__in = submission_data):
                    assessment_items[a.submission_datum.id] = a.serialize()

                submission_data_items = [d.serialize() for d in submission_data]
                for d in submission_data_items:
                    d["assessment"] = assessment_items.get(d["id"])
                    
                data = {"submissions": submission_data_items}
                response = Response(data)
            else:
                response = Response(status = 404)
        else:
            response = Response(status = 404)
    else:
        response = Response(status = 404)
    return response
