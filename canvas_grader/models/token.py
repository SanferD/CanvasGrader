from django.db import models
from .domain import Domain
from server import settings

class Profile(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length = 50, blank = False, null = False)

    class Meta:
        unique_together = ("user_id", "name")

class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    token = models.CharField(max_length=66, blank = False, null = False)
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete = models.CASCADE)
    
    class Meta:
        unique_together = ("token", "domain")

