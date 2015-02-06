from django.db import models
from django.conf import settings

class Vote(models.Model):
    question = models.CharField(max_length=512)
    extra_description = models.TextField(max_length=4096)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)

class Choice(models.Model):
    question = models.ForeignKey(Vote)
    choice_text = models.CharField(max_length=512)

class CastVote(models.Model):
    choice = models.ForeignKey(Choice)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL)
