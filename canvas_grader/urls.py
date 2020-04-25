from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index), 
    path('settings', views.Settings),
    path('tokens', views.Tokens.as_view()),
    path('domains/<int:domain_id>/courses', views.GetCourses),
    path('courses/<int:course_id>/quizzes', views.GetQuizzes),
    path('quizzes/<int:quiz_id>/grading-views', views.GradingAPIViews.as_view()),
    path('quizzes/<int:quiz_id>/grading-views/add', views.AddGradingView),
    path('quizzes/<int:quiz_id>/questions', views.GetAllQuizQuestions),
    path('grading-views/<int:view_id>/grading-groups', views.GetGradingGroups),
]

