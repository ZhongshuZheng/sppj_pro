from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=8, null=True)
    address = models.CharField(max_length=150, null=True)
    contacts = models.CharField(max_length=25, null=True)
    telephone = models.CharField(max_length=20, null=True)
    setupdate = models.DateField(null=True)
    legalpersoncode = models.CharField(max_length=30, null=True, unique=True)
    legalpersoncode_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    zipcode = models.CharField(max_length=6, null=True)
    superiordepartment = models.CharField(max_length=50, null=True)
    assets = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    capital = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    qualification = models.CharField(max_length=25, null=True)
    qualification_date = models.DateField(null=True)
    qualification_file = models.FileField(upload_to="/upload_file/", null=True)    # try and finish
    quality = models.CharField(max_length=25, null=True)
    quality_date = models.DateField(null=True)
    quality_file = models.FileField(ull=True)
    artisan_sum = models.IntegerField(null=True)
    artisan_m_sum = models.IntegerField(null=True)
    artisan_h_sum = models.IntegerField(null=True)
    artisan_e_sum = models.IntegerField(null=True)
    artisan_mj_sum = models.IntegerField(null=True)
    artisan_en_sum = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    fax = models.CharField(max_length=20, null=True)
    request_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    explain_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    lisence_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    system_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    assets_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    equipment_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    place_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    score = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    begintime = models.DateField(null=True)
    endtime = models.DateField(null=True)
    continuetimes = models.IntegerField(null=True)
    suggestion = models.TextField(null=True)
    examiner = models.ForeignKey('users.User', null=True)
    examiner_time = models.DateField()
    examine_statue = models.CharField(max_length=1, default='1')
        # 1 is examining, 2 is examined, 3 is examine failed
    inblack = models.CharField(max_length=1, default=0)  # 0 is not, 1 is in


class PeopleInfo(models.Model):
    name = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=2, null=True)
    title = models.CharField(max_length=15, null=True)
    title_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    major = models.CharField(max_length=30, null=True)
    major_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    idnum_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish

    class Meta:
        abstract = True


class StackHolder(PeopleInfo):
    post = models.CharField(max_length=30, null=True)
    telephone = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    train_code = models.CharField(max_length=100, null=True)
    resume = models.TextField(null=True)
    company = models.ForeignKey('Company')
    types = models.ManyToManyField('StackHolderType', null=True)


class StackHolderType(models.Model):
    name = models.CharField(max_length=1)   # 0, 1, 2


class Artisan(PeopleInfo):
    education = models.CharField(max_length=50, null=True)
    company = models.ForeignKey('Company')


class Certificate(models.Modle):
    num = models.CharField(max_length=100, null=True)
    time = models.DateField(null=True)
    type = models.CharField(max_length=1, null=True)    # 0, 1
    file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    artisan = models.ForeignKey('Artisan')


class Project(models.Model):
    name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=10, null=True)
    level = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    investment = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    investment_sb = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    assumemethod = models.CharField(max_length=1, null=True)    # 0, 1
    time = models.CharField(max_length=50, null=True)
    approval = models.CharField(max_length=100, null=True)
    approval_file = models.FileField(upload_to="/upload_file/", null=True)  # try and finish
    company = models.ForeignKey('Company')
