from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel
from canvas_grader.models import fields as cgf
from .domain import Course

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

