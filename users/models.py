from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    signid = models.CharField(max_length=30)
    password = models.CharField(max_length=25)
    email = models.EmailField()
    idnumber = models.CharField(max_length=19)
    type = models.CharField(max_length=1, default='1')  # 0 is admin, and 1 is company
    company = models.ForeignKey('companies.Company', null=True)
