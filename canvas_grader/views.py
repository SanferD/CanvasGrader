from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from canvas_grader.models import Domain, Token, Profile, Course, \
                                 CourseLink, Quiz, GradingView, \
                                 GradingGroup, GroupQuestionLink, \
                                 QuizQuestion, Submission, AssessmentItem, \
                                 Assignment, SubmissionDatum
from canvas_grader import api
from canvas_grader import controllers
import collections

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
        controllers.PopulateCoursesOnly(token)

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
        links = CourseLink.objects.filter(user = user, course__domain = domain)
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

def EditGradingView(request, quiz_id, grading_view_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        grading_view = GradingView.objects.filter(id = grading_view_id).first()
        if grading_view:
            grading_groups = GradingGroup.objects.filter(grading_view = grading_view)
            ggs = list()
            for gg in grading_groups:
                d = gg.serialize()
                questions = [l.quiz_question.id for l in GroupQuestionLink.objects.filter(grading_group = gg)]
                d["questions"] = questions
                ggs.append(d)
            grading_view = grading_view.serialize()
            grading_view.pop("date_created")
            grading_view["grading_groups"] = ggs
            data = {"domain": course.domain, "course": course,
                    "quiz": quiz, "grading_view": grading_view,
                    "grading_groups": ggs}
            response = render(request, "grading/grading-view.html", data)
        else:
            response = Response(status = 404)
    else:
        response = Response(status = 404)
    return response
    

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def GetAllQuizQuestions(request, quiz_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        questions = [{"id": q.id, "question_name": q.question_name} for q in quiz.quizquestion_set.all()]
        response = Response(questions)
    else:
        response = Response(status = 404)
    return response

class GradingAPIViews(views.APIView):
    def get(self, request, quiz_id):
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            grading_views = GradingView.objects.filter(quiz = quiz)
            gvs = [gv.serialize() for gv in grading_views]
            for g in gvs:
                g.pop("date_created")
            data = {"domain": course.domain, "course": course,
                    "quiz": quiz, "grading_views": gvs}
            response = render(request, "resources/grading-views.html", data)
        else:
            response = Response(status = 404)
            
        return response

    def post(self, request, quiz_id):
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            data = request.data["grading_view"]
            if "id" in data:
                GradingView.objects.get(id = data["id"]).delete()
                grading_view = GradingView(id = data["id"],
                                quiz = quiz, name = data["name"])
                grading_view.save()
            else:
                grading_view, _ = GradingView.objects.get_or_create(
                                    quiz = quiz, name = data["name"])
            for g in data["grading_groups"]:
                grading_group, _ = GradingGroup.objects.get_or_create(
                                    name = g["name"], grading_view = grading_view)
                for q in g["questions"]:
                    link, _ = GroupQuestionLink.objects.get_or_create(
                                    quiz_question = QuizQuestion.objects.get(id = q),
                                    grading_group = grading_group)
            response = Response(status = 200)
        else:
            response = Response(status = 404)
        return response

    def delete(self, request, quiz_id):
        course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
        if is_valid:
            gid = request.data["grading_view"]
            grading_view = GradingView.objects.filter(id = gid).first()
            if grading_view:
                grading_view.delete()
                response = Response(status = 200)
            else:
                response = Response(status = 404)
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
    view = GradingView.objects.filter(id = view_id).first()

    quiz_id = view.quiz.id if view else None
    if quiz_id:
        _, _, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    else:
        is_valid = False
    return view, is_valid

def QuizId2CourseQuizValid(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.filter(id = quiz_id).first()

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
                qt = q["question_text"]
                q["question_text"] = '\\"'.join(  qt.split('"')  )

            submissions = Submission.objects.filter(assignment__quiz = quiz).order_by("canvas_user__sortable_name")
            canvas_users = [s.canvas_user.serialize() for s in submissions]
            for u in canvas_users:
                n = u["name"]
                u["name"] = "".join(n.split("'"))
                u.pop("sortable_name")
            data = {"quiz": quiz, "questions": questions,
                    "domain": course.domain, "course": course,
                    "canvas_users": canvas_users,
                    "grading_group": grading_group,
                    "grading_view": grading_group.grading_view}
            response = render(request, "grader/grader.html", data)
        else:
            response = Response(status = 404)
    else:
        response = Response(status = 404)
    return response

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def GetGradedCanvasUsers(request, quiz_id, grading_group_id):
    course, quiz, is_valid = QuizId2CourseQuizValid(request, quiz_id)
    if is_valid:
        grading_group = GradingGroup.objects.filter(id = grading_group_id).first()
        if grading_group:
            questions = [l.quiz_question for l in grading_group.groupquestionlink_set.all()]
            items = AssessmentItem.objects.filter(
                            submission_datum__quiz_question__in = questions)
            users = collections.defaultdict(set)
            for i in items:
                cu = i.submission_datum.submission_history_item.submission.canvas_user
                q = i.submission_datum.quiz_question
                users[cu].add(q)

            graded_users = []
            q_len = len([q for q in questions if q.question_type != "text_only_question"])
            for cu, qs in users.items():
                if len(qs) == q_len:
                    graded_users.append(cu.id)
            response = Response(graded_users)
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

class QuizImport(views.APIView):
    def get(self, request, course_id):
        user = request.user
        course_link = CourseLink.objects.filter(user = user, course__id = course_id).first()
        if course_link:
            course = course_link.course
            token = Token.objects.get(user = user, domain = course.domain)
            api_course = api.GetCourse(token, course.course_id)
            api_quiz_assignments = api.GetQuizAssignments(api_course)
            api_quizzes = [[a.attributes["id"], a.attributes["name"]] for a in api_quiz_assignments]
            assignments = Assignment.objects.filter(course = course)
            db_quizzes = [[a.assignment_id, a.name] for a in assignments]
            api_quizzes.sort()
            db_quizzes.sort()
            data = {"api_quizzes": api_quizzes, "db_quizzes": db_quizzes,
                    "domain": course.domain, "course": course}
            response = render(request, "quizzes/import.html", data)
        else:
            response = Response(status = 404)
        return response

    def post(self, request, course_id):
        user = request.user
        course_link = CourseLink.objects.filter(user = user, course__id = course_id).first()
        if course_link:
            course = course_link.course
            token = Token.objects.get(user = user, domain = course.domain)
            assignment_ids = [x[0] for x in request.data]
            api_course = api.GetCourse(token, course.course_id)
            all_quiz_assignments = api.GetQuizAssignments(api_course)
            api_quiz_assignments = [x for x in all_quiz_assignments if x.attributes["id"] in assignment_ids]
            for api_quiz_assignment in api_quiz_assignments:
                controllers.PopulateQuizOnly(course, api_course, api_quiz_assignment)
            response = Response(status = 204)
        else:
            response = Response(status = 404)
        return response
     
@api_view(['POST'])
def SaveAssessment(request, datum_id):
    user = request.user
    datum = SubmissionDatum.objects.filter(id = datum_id).first()
    if datum:
        course = datum.submission_history_item.submission.assignment.course
        link = CourseLink.objects.filter(user=user, course=course).first()
        if link:
            contents = request.data
            assessment_data = contents.get("assessment")
            assessment_item = AssessmentItem.objects.filter(submission_datum = datum).first()
            if not assessment_item:
                assessment_item = AssessmentItem(submission_datum = datum)
            try:
                assessment_item.score = float(assessment_data["score"])
            except:
                pass
            comment = assessment_data.get("comment", "").strip()
            if comment:
                assessment_item.comment = comment
            assessment_item.save()
            token = Token.objects.get(user = user, domain = course.domain)
            controllers.UpdateScoreAndComments(token, assessment_item)
            return Response(status = 200)
        else:
            response = Response(status = 404)
    else:
        response = Response(status = 404)
    return response
    

