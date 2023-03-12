from django.db import models
from datetime import datetime

class UserOfFacility(models.Model):
    user_id = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    address = models.TextField(default="", max_length=300)
    tel = models.CharField(max_length=11)
    mail = models.CharField(max_length=30)
    handicap_name = models.TextField(default="", max_length=300)
    handicap_level = models.IntegerField(blank=True, null=True)

    def __str__(self):
      return self.name

class CaseReport(models.Model):
    user_id = models.IntegerField(default=0)
    occurrence_date = models.DateTimeField(default=datetime.now())
    name = models.CharField(max_length=50)
    case_name = models.CharField(max_length=50)
    content = models.TextField(default="")
    method = models.TextField(default="")
    result = models.TextField(default="")

    def __str__(self):
      return self.case_name