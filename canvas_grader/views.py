from django.shortcuts import render

def index(request):
    response = render(request, "login/login.html", {})
    return response
        
