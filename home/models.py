from django.db import models


class AgencySurvey(models.Model):
    name = models.CharField(max_length=60)
    survey = models.TextField()

