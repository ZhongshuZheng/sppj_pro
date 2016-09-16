from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):

    def create_user(self, signid, email, idnumber, itype, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not signid:
            raise ValueError('Users must have an id')

        user = User(
            signid=signid,
            email=self.normalize_email(email),
            idnumber=idnumber,
            itype=itype,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def change_user(self, signid, email, idnumber):
        user = User.objects.get(signid=signid)
        user.email = email
        user.idnumber = idnumber
        user.save()


# Create your models here.
class User(AbstractBaseUser):
    signid = models.CharField(max_length=30, unique=True, default="")
    # password = models.CharField(max_length=25)
    email = models.EmailField()
    idnumber = models.CharField(max_length=19, default="")
    itype = models.CharField(max_length=1, default='1')  # 0 is admin, and 1 is company, 2 is deleted
    company = models.ForeignKey('companies.Company', null=True)
    passkey = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'signid'
    REQUIRED_FIELDS = ['email', 'idnumber', 'itype']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.signid

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
