from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from canvas_grader.models import Token

def Index(request):
    if request.user.is_authenticated:
        domains = []
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
                f(user, token)
            response = Response(status = 200)
        else:
            response = Response(status = 400)
        return response

    def __createOrUpdateToken(self, user, token):
        print("create", token)

    def __deleteToken(self, user, token):
        print("delete", token)

