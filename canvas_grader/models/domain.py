from django.db import models

class Domain(models.Model):
    url = models.URLField(max_length = 20)


