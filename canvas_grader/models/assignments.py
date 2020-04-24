from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel
from canvas_grader.models import fields as cgf
from .domain import Course

class UnknownQuestionType(Exception):
    def __init__(self, qt):
        message = "unknown question type: {}".format(qt)
        Exception.__init__(self, message)

class Assignment(FkSerializableModel):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    assignment_id = cgf.CanvasIdField()
    name = models.CharField(max_length = 50, blank = False, null = False)
    points_possible = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    html_url = models.URLField()

    class Meta:
        unique_together = ("assignment_id", "course")

class Quiz(FkSerializableModel):
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    quiz_id = cgf.CanvasIdField()
    speed_grader_url = models.URLField(null = True)
    question_count = models.IntegerField()

    class Meta:
        unique_together = ("assignment", "quiz_id")

class QuizQuestionGroup(FkSerializableModel):
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    group_id = cgf.CanvasIdField()

    class Meta:
        unique_together = ("quiz", "group_id")

class QuizQuestion(FkSerializableModel):
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    question_id = cgf.CanvasIdField()
    question_name = models.CharField(max_length = 100, blank = False, null = False)
    question_text = models.TextField()
    quiz_question_group = models.ForeignKey(QuizQuestionGroup, on_delete = models.CASCADE, null = True)
    question_type = models.CharField(max_length = 50)
    points_possible = models.FloatField()

    class Meta:
        unique_together = ("quiz", "question_id")

