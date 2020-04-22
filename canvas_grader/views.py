from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        domains = []
        response = render(request, "resources/domains.html", {"domains": domains})
    else:
        response = render(request, "login/login.html", {})
    return response
        
