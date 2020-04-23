from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index), 
    path('settings', views.Settings),
    path('tokens', views.Tokens.as_view()),
    path('domains/<int:domain_id>/courses', views.GetCourses),
    path('courses/<int:course_id>/quizzes', views.GetQuizzes),
]

