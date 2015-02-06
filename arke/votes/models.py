from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Vote(models.Model):
    question = models.CharField(max_length=512)
    extra_description = models.TextField(max_length=4096, blank=True)
    category = models.ForeignKey(Category, default=1)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{}/{}'.format(self.submitter, self.question)


class Choice(models.Model):
    question = models.ForeignKey(Vote)
    choice_text = models.CharField(max_length=512)

    def __str__(self):
        return '{}/{}'.format(self.choice_text, self.question)


class CastVote(models.Model):
    choice = models.ForeignKey(Choice)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{}/{}'.format(self.voter, self.choice)
