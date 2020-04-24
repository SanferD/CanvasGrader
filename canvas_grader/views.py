from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from canvas_grader.models import Domain, Token, Profile, Course, CourseLink, Quiz, GradingView
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
        tokens = [t.serialize() for t in tokens]
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
        if id:
            token = Token.objects.get(id = id)
            token.token = api_token
            token.domain = domain
        else:
            defaults = {"name": u["name"]}
            profile, _ = Profile.objects.get_or_create(
                            user_id = u["id"], defaults = defaults)
            token = Token(
                        user = user, token = api_token,
                        domain = domain, profile = profile)
        token.save()
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

def GetGradingViews(request, quiz_id):
    user = request.user
    try:
        quiz = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        quiz = None

    if quiz:
        course = quiz.assignment.course
        is_valid = CourseLink.objects.filter(user = user, course = course).count() != 0
    else:
        is_valid = False

    if is_valid:
        grading_views = GradingView.objects.filter(quiz = quiz)
        data = {"domain": course.domain, "course": course,
                "quiz": quiz, "grading_views": grading_views}
        response = render(request, "resources/grading-views.html", data)
    else:
        response = Response(status = 404)
        
    return response

