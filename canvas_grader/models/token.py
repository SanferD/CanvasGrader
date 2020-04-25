from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel
from .domain import Domain
from server import settings
from canvas_grader.models import fields as cgf

class Profile(FkSerializableModel):
    user_id = cgf.CanvasIdField()
    name = models.CharField(max_length = 50, blank = False, null = False)

    class Meta:
        unique_together = ("user_id", "name")

    def __str__(self):
        return self.name

class Token(FkSerializableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    token = models.CharField(max_length=100, blank = False, null = False)
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("token", "domain")

    def __str__(self):
        return "token for {} on {}".format(str(self.user), self.domain.url)

