from django.db import models
from .assignments import Assignment, QuizQuestion
from .domain import Domain
from canvas_grader.models.serializable_model import FkSerializableModel
from canvas_grader.models import fields as cgf

class CanvasUser(FkSerializableModel):
    user_id = cgf.CanvasIdField()
    name = models.CharField(max_length = 50, blank = False, null = False)
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("user_id", "domain")

class Submission(FkSerializableModel):
    submission_id = cgf.CanvasIdField()
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    posted_at = models.DateTimeField(null = True)
    preview_url = models.URLField()
    canvas_user = models.OneToOneField(CanvasUser, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("assignment", "submission_id")

class SubmissionHistoryItem(FkSerializableModel):
    submission = models.ForeignKey(Submission, on_delete = models.CASCADE)
    submission_history_id = cgf.CanvasIdField()

    class Meta:
        unique_together = ("submission", "submission_history_id")

class SubmissionDatum(FkSerializableModel):
    submission_history_item = models.ForeignKey(SubmissionHistoryItem, on_delete = models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ("quiz_question", "submission_history_item")

