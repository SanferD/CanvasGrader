from django.db import models

class CanvasIdField(models.IntegerField):
    description = "A wrapper class to represent canvas ids"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

