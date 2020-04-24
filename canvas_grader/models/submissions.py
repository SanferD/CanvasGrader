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

    def __str__(self):
        return self.name

class Submission(FkSerializableModel):
    submission_id = cgf.CanvasIdField()
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    posted_at = models.DateTimeField(null = True)
    preview_url = models.URLField()
    canvas_user = models.OneToOneField(CanvasUser, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("assignment", "submission_id")

    def __str__(self):
        return "submission by {} for {}".format(str(self.canvas_user), str(self.assignment))

class SubmissionHistoryItem(FkSerializableModel):
    submission = models.ForeignKey(Submission, on_delete = models.CASCADE)
    submission_history_id = cgf.CanvasIdField()

    class Meta:
        unique_together = ("submission", "submission_history_id")
    
    def __str__(self):
        return "submission history item {} for {}".format(self.submission_history_id, str(self.submission))

class SubmissionDatum(FkSerializableModel):
    submission_history_item = models.ForeignKey(SubmissionHistoryItem, on_delete = models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete = models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ("quiz_question", "submission_history_item")
    
    def __str__(self):
        u = self.submission_history_item.submission.canvas_user
        return "submission for {} by {}".format(str(self.quiz_question), str(u))

class AssessmentItem(FkSerializableModel):
    submission_datum = models.OneToOneField(SubmissionDatum, on_delete = models.CASCADE)
    score = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return "assessment for {}".format(str(self.submission_datum))

