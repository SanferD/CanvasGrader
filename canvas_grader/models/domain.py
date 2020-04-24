from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel
from canvas_grader.models import fields as cgf
from server import settings

class Domain(FkSerializableModel):
    url = models.URLField(max_length = 30)

    def __str__(self):
        return self.url

class Course(FkSerializableModel):
    course_id = cgf.CanvasIdField()
    name = models.CharField(max_length = 100, blank = False, null = False)
    created_at = models.DateTimeField()
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("course_id", "domain")

    def __str__(self):
        return self.name

class CourseLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return "{}: {}".format(str(self.user), str(self.course))

