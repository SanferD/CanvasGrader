from django.db import models
from canvas_grader.models.serializable_model import FkSerializableModel

class Domain(FkSerializableModel):
    url = models.URLField(max_length = 30)

