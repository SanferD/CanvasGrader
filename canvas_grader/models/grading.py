from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel
from canvas_grader.models import fields as cgf
from .assignments import Quiz, QuizQuestion
from server import settings

class GradingView(FkSerializableModel):
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, blank = False, null = False)
    date_created = models.DateTimeField(auto_now = False, auto_now_add = True)

    class Meta:
        unique_together = ("quiz", "name")

    def __str__(self):
        return "grading view {} for quiz {}".format(self.name, str(self.quiz))

class GradingGroup(FkSerializableModel):
    name = models.CharField(max_length = 50, blank = False, null = False)
    grading_view = models.ForeignKey(GradingView, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("name", "grading_view")

    def __str__(self):
        return "grading group {} for grading view {}".format(self.name, str(self.grading_view))

class GroupQuestionLink(FkSerializableModel):
    quiz_question = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE)
    grading_group = models.ForeignKey(GradingGroup, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("quiz_question", "grading_group")

    def __str__(self):
        return "quiz_question: {}; grading_group: {}".format(str(self.quiz_question), str(self.grading_group))

