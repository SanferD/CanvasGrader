from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from canvas_grader.models import Domain, Token, Profile
from canvas_grader import api

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
        id, api_token, domain_url = data.get("id"), data["token"], data["domain"]
        domain, _ = Domain.objects.get_or_create(url = domain_url)
        if id:
            token = Token.objects.get(id = id)
            token.token = api_token
            token.domain = domain
        else:
            u = api.GetCurrentUser(domain_url, api_token).attributes
            profile, _ = Profile.objects.get_or_create(user_id = u["id"], defaults = {"name": u["name"]})
            token = Token(user = user, token = api_token, domain = domain, profile = profile)
        token.save()

    def __deleteToken(self, user, data):
        id = data.get("id")
        if id:
            Token.objects.get(id = id).delete()

