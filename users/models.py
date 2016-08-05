from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_signid = models.CharField(max_length=30)
    user_password = models.CharField(max_length=25)
    user_email = models.EmailField()
    user_idnumber = models.CharField(max_length=19)
    user_type = models.CharField(max_length=1, default='1')  # 0 is admin, and 1 is company
    user_examiner_id = models.ForeignKey('self', null=True)
    user_examiner_time = models.DateField()
    user_examine_statue = models.CharField(max_length=1, default='1')
        # 1 is examining, 2 is examined, 3 is examine failed
    user_inblack = models.CharField(max_length=1, default=0)  # 0 is not, 1 is in
