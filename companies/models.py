# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os

from django.db import models


# Managers here.
from sppj.settings import BASE_DIR


class CompanyManager(models.Manager):

    @staticmethod
    def del_old_file(orifile):
        """
        :param orifile: the file need to be delete
        :return:
        """
        try:
            old_file = orifile.path
            print "finding ", old_file
            if os.path.exists(old_file):
                print "deleting ", old_file
                os.remove(old_file)
        except:
            pass

    @staticmethod
    def change_file_path(pk, thefile, thestring, other_mes=''):
        """
        :param pk: the unique name, just to provide the name for file
        :param thefile: the whole object of company.file
        :param thestring: the string name of company.file
        :param other_mes: if you want to add sth. after the file name
        :return:
        """
        pk = str(pk)
        initial_path = thefile.path
        thefile.name = "assets/upload_file/" + thestring + "/" + pk + "_" + thestring\
                       + other_mes + "." + thefile.name.split(".")[-1]
        new_path = BASE_DIR + '/' + thefile.name
        # print new_path
        # print "    " + initial_path
        # print thefile.path
        try:
            os.rename(initial_path, new_path)
        except:
            CompanyManager.del_old_file(initial_path)

    @staticmethod
    def page_one_save(info, user, new_file=0):
        company = user.company
        if not company:
            company = Company()
            # print 'a new one.'
        company.name = info['name']
        # company.grade = info['grade']
        company.itype = info['itype']
        company.address_a = info['address_a']
        company.address_b = info['address_b']
        company.address_c = info['address_c']
        company.isgroup = info['isgroup']
        company.phone = info['phone']
        company.contacts = info['contacts']
        company.telephone = info['telephone']
        company.Company_work_begin = info['Company_work_begin']
        company.Company_work_end = info['Company_work_end']
        company.telephone = info['telephone']
        company.setupdate = datetime.date.today()
        # company.legalpersoncode = info['legalpersoncode']
        # if new_file == 1:
        #     # delete the origin file if exist
        #     CompanyManager.del_old_file(company.legalpersoncode_file)
        #     company.legalpersoncode_file = info['legalpersoncode_file']
        company.zipcode = info['zipcode']
        company.zipcodeplace = info['zipcodeplace']
        company.creditcode = info['creditcode']
        # company.superiordepartment = info['superiordepartment']
        company.assets = info['assets']
        # company.capital = info['capital']
        company.email = info['email']
        company.fax = info['fax']
        company.examine_statue = '3'
        company.score = '0'
        company.save()

        # # change the name of the file
        # if new_file == 1:
        #     CompanyManager.change_file_path(company.id, company.legalpersoncode_file,
        #                                     "legalpersoncode_file")
        #     company.save()

        # user foreigner key
        user.company = company
        user.save()

    @staticmethod
    def page_two_save(info, user, request):
        company = user.company

        # company.qualification = info['qualification']
        # company.qualification_date = info['qualification_date']
        # if 'qualification_file' in request.FILES:
        #     CompanyManager.del_old_file(company.qualification_file)
        #     company.qualification_file = info['qualification_file']
        if 'quality_file' in request.FILES:
            CompanyManager.del_old_file(company.quality_file)
            company.quality_file = info['quality_file']
        if 'request_file' in request.FILES:
            CompanyManager.del_old_file(company.request_file)
            company.request_file = info['request_file']
        if 'explain_file' in request.FILES:
            CompanyManager.del_old_file(company.explain_file)
            company.explain_file = info['explain_file']
        # if 'lisence_file' in request.FILES:
        #     CompanyManager.del_old_file(company.lisence_file)
        #     company.lisence_file = info['lisence_file']
        if 'system_file' in request.FILES:
            CompanyManager.del_old_file(company.system_file)
            company.system_file = info['system_file']
        # if 'assets_file' in request.FILES:
        #     CompanyManager.del_old_file(company.assets_file)
        #     company.assets_file = info['assets_file']
        # if 'equipment_file' in request.FILES:
        #     CompanyManager.del_old_file(company.equipment_file)
        #     company.equipment_file = info['equipment_file']
        if 'place_file' in request.FILES:
            CompanyManager.del_old_file(company.place_file)
            company.place_file = info['place_file']
        if 'legalpersoncode_file' in request.FILES:
            CompanyManager.del_old_file(company.legalpersoncode_file)
            company.legalpersoncode_file = info['legalpersoncode_file']
        company.save()

        # change the name of the file
        # if 'qualification_file' in request.FILES:
        #     CompanyManager.change_file_path(company.id, company.qualification_file, "qualification_file")
        if 'quality_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.quality_file, "quality_file")
        if 'request_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.request_file, "request_file")
        if 'explain_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.explain_file, "explain_file")
        if 'lisence_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.lisence_file, "lisence_file")
        if 'system_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.system_file, "system_file")
        if 'legalpersoncode_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.legalpersoncode_file, "legalpersoncode_file")
        # if 'assets_file' in request.FILES:
        #     CompanyManager.change_file_path(company.id, company.assets_file, "assets_file")
        # if 'equipment_file' in request.FILES:
        #     CompanyManager.change_file_path(company.id, company.equipment_file, "equipment_file")
        if 'place_file' in request.FILES:
            CompanyManager.change_file_path(company.id, company.place_file, "place_file")
        company.save()

    @staticmethod
    def page_three_save(info, user, request, idnum):
        company = user.company
        types = info['types']
        try:
            holder = company.stackholder.get(types=types)
        except:
            holder = StackHolder()

        holder.name = info['name']
        holder.phone = info['phone']
        holder.sex = info['sex']
        holder.birthd = info['birthd']
        holder.title = info['title']
        holder.titlemajor = info['titlemajor']
        if 'title_file' in request.FILES:
            CompanyManager.del_old_file(holder.title_file)
            holder.title_file = info['title_file']
        holder.major = info['major']
        if 'major_file' in request.FILES:
            CompanyManager.del_old_file(holder.major_file)
            holder.major_file = info['major_file']
        if 'idnum_file' in request.FILES:
            CompanyManager.del_old_file(holder.idnum_file)
            holder.idnum_file = info['idnum_file']
        holder.telephone = info['telephone']
        holder.email = info['email']
        # holder.train_code = info['train_code']
        holder.resume = info['resume']
        holder.types = info['types']
        if info['types'] == '1' and 'work_year' in info:
            company.three_check = '1'
            company.save()
            holder.work_year = info['work_year']
            if 'work_file' in request.FILES:
                CompanyManager.del_old_file(holder.work_file)
                holder.work_file = info['work_file']
        holder.idnum = idnum
        holder.company = company

        holder.save()

        # change the name of the file
        if 'title_file' in request.FILES:
            CompanyManager.change_file_path(holder.id, holder.title_file,
                                            "title_file", other_mes='_sh' + info['types'])
        if 'major_file' in request.FILES:
            CompanyManager.change_file_path(holder.id, holder.major_file,
                                            "major_file", other_mes='_sh' + info['types'])
        if 'idnum_file' in request.FILES:
            CompanyManager.change_file_path(holder.id, holder.idnum_file,
                                            "idnum_file", other_mes='_sh' + info['types'])
        if 'work_file' in request.FILES:
            CompanyManager.change_file_path(holder.id, holder.idnum_file,
                                            "work_file", other_mes='_sh' + info['types'])
        holder.save()

    @staticmethod
    def page_four_save(info, user, request, idnum, ori_idnum):

        company = user.company

        try:
            people = Artisan.objects.get(idnum=ori_idnum)
        except:
            people = Artisan()
        people.name = info['name']
        people.sex = info['sex']
        people.birthd = info['birthd']
        people.title = info['title']
        people.titlemajor = info['titlemajor']
        if 'title_file' in request.FILES:
            CompanyManager.del_old_file(people.title_file)
            people.title_file = info['title_file']
        people.major = info['major']
        if 'major_file' in request.FILES:
            CompanyManager.del_old_file(people.major_file)
            people.major_file = info['major_file']
        if 'idnum_file' in request.FILES:
            CompanyManager.del_old_file(people.idnum_file)
            people.idnum_file = info['idnum_file']
        if 'onjob_file' in request.FILES:
            CompanyManager.del_old_file(people.onjob_file)
            people.onjob_file = info['onjob_file']
        people.education = info['education']
        people.idnum = idnum
        people.company = company

        people.save()

        # the Certificates
        # file0
        if 'file_0' in request.POST:
            try:
                file0 = people.certificate.get(itype='0')
            except:
                file0 = Certificate()
                file0.itype = '0'
            file0.num = info['file_num0']
            file0.time = info['file_time0']
            if 'file_file0' in request.FILES:
                CompanyManager.del_old_file(file0.file)
                file0.file = info['file_file0']
            file0.artisan = people
            file0.save()
        else:
            try:
                file0 = people.certificate.get(itype='0')
            except:
                pass
            else:
                CompanyManager.del_old_file(file0.file)
                file0.delete()
        # file1
        if 'file_1' in request.POST:
            try:
                people.certificate.get(itype='1')
            except:
                file1 = Certificate()
                file1.itype = '1'
            else:
                file1 = people.certificate.get(itype='1')
            file1.num = info['file_num1']
            file1.time = info['file_time1']
            if 'file_file1' in request.FILES:
                CompanyManager.del_old_file(file1.file)
                file1.file = info['file_file1']
            file1.artisan = people
            file1.save()
        else:
            try:
                file1 = people.certificate.get(itype='1')
            except:
                pass
            else:
                CompanyManager.del_old_file(file1.file)
                file1.delete()

        # change the name of the files
        if 'title_file' in request.FILES:
            CompanyManager.change_file_path(people.id, people.title_file,
                                            "title_file", other_mes='_art')
        if 'major_file' in request.FILES:
            CompanyManager.change_file_path(people.id, people.major_file,
                                            "major_file", other_mes='_art')
        if 'idnum_file' in request.FILES:
            CompanyManager.change_file_path(people.id, people.idnum_file,
                                            "idnum_file", other_mes='_art')
        if 'onjob_file' in request.FILES:
            CompanyManager.change_file_path(people.id, people.onjob_file,
                                            "onjob_file", other_mes='_art')
        if 'file_0' in request.POST and 'file_file0' in request.FILES:
            CompanyManager.change_file_path(people.id, file0.file,
                                            "certificates_file", other_mes='_0')
            file0.save()
        if 'file_1' in request.POST and 'file_file1' in request.FILES:
            CompanyManager.change_file_path(people.id, file1.file,
                                            "certificates_file", other_mes='_1')
            file1.save()
        people.save()

    @staticmethod
    def page_five_save(info, user, request, approval, ori_approval):

        company = user.company

        try:
            project = Project.objects.get(approval=ori_approval)
        except:
            project = Project()
        project.name = info['name']
        project.itype = info['itype']
        project.level = info['level']
        project.address_a = info['address_a']
        project.address_b = info['address_b']
        project.address_c = info['address_c']
        project.build_company = info['build_company']
        project.department = info['department']
        project.investment = info['investment']
        # project.investment_sb = info['investment_sb']
        # project.assumemethod = info['assumemethod']
        project.time = info['time']
        project.timebef = info['timebef']
        project.approval = approval
        if 'approval_a_file' in request.FILES:
            CompanyManager.del_old_file(project.approval_a_file)
            project.approval_a_file = info['approval_a_file']
        if 'approval_b_file' in request.FILES:
            CompanyManager.del_old_file(project.approval_b_file)
            project.approval_b_file = info['approval_b_file']
        if 'approval_c_file' in request.FILES:
            CompanyManager.del_old_file(project.approval_c_file)
            project.approval_c_file = info['approval_c_file']
        if 'contract_file' in request.FILES:
            CompanyManager.del_old_file(project.contract_file)
            project.contract_file = info['contract_file']
        project.company = company

        project.save()

        # change the name of the files
        if 'approval_a_file' in request.FILES:
            CompanyManager.change_file_path(project.id, project.approval_a_file,
                                            "approval_a_file", other_mes='_proj')
        if 'approval_b_file' in request.FILES:
            CompanyManager.change_file_path(project.id, project.approval_b_file,
                                            "approval_b_file", other_mes='_proj')
        if 'approval_c_file' in request.FILES:
            CompanyManager.change_file_path(project.id, project.approval_c_file,
                                            "approval_c_file", other_mes='_proj')
        if 'contract_file' in request.FILES:
            CompanyManager.change_file_path(project.id, project.contract_file,
                                            "contract_file", other_mes='_proj')
        project.save()

    @staticmethod
    def delete_aritsan(idnum):
        """
        To del a artisan and all his files.
        :param idnum:
        :return:
        """
        artisan = Artisan.objects.get(idnum=idnum)
        # if artisan not in get_user(request).company.artisan.all() or get_user(request).itype != 0:
        #     return redirect('index')
        for i in artisan.certificate.all():
            CompanyManager.del_old_file(i.file)
            i.delete()
        CompanyManager.del_old_file(artisan.title_file)
        CompanyManager.del_old_file(artisan.major_file)
        CompanyManager.del_old_file(artisan.idnum_file)
        artisan.delete()

    @staticmethod
    def delete_project(approval):
        """
        To del a project and all his files.
        :param approval:
        :return:
        """
        project = Project.objects.get(approval=approval)
        # if artisan not in get_user(request).company.artisan.all() or get_user(request).itype != 0:
        #     return redirect('index')
        CompanyManager.del_old_file(project.approval_file)
        CompanyManager.del_old_file(project.contract_file)
        project.delete()


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100, null=True)
    address_a = models.CharField(max_length=50, null=True)
    address_b = models.CharField(max_length=50, null=True)
    address_c = models.CharField(max_length=50, null=True)
    itype = models.CharField(max_length=50, null=True)
    isgroup = models.CharField(max_length=2, null=True)     # 0 is no and 1 is yes!
    phone = models.CharField(max_length=16, null=True)
    creditcode = models.CharField(max_length=50, null=True)
    contacts = models.CharField(max_length=25, null=True)
    telephone = models.CharField(max_length=20, null=True)
    setupdate = models.DateField(null=True)
    legalpersoncode_file = models.FileField(upload_to="assets/upload_file/legalpersoncode_file/", null=True)  # try and finish
    zipcode = models.CharField(max_length=6, null=True)
    zipcodeplace = models.CharField(max_length=100, null=True)
    assets = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quality_file = models.FileField(upload_to="assets/upload_file/quality_file/", null=True)
    artisan_sum = models.IntegerField(null=True)
    artisan_m_sum = models.IntegerField(null=True)
    artisan_h_sum = models.IntegerField(null=True)
    artisan_e_sum = models.IntegerField(null=True)
    artisan_mj_sum = models.IntegerField(null=True)
    artisan_en_sum = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    fax = models.CharField(max_length=20, null=True)
    request_file = models.FileField(upload_to="assets/upload_file/request_file/", null=True)  # try and finish
    explain_file = models.FileField(upload_to="assets/upload_file/explain_file/", null=True)  # try and finish
    system_file = models.FileField(upload_to="assets/upload_file/system_file/", null=True)  # try and finish
    place_file = models.FileField(upload_to="assets/upload_file/place_file/", null=True)  # try and finish
    score = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    begintime = models.DateField(null=True)
    endtime = models.DateField(null=True)
    Company_work_begin = models.DateField(null=True)
    Company_work_end = models.DateField(null=True)
    continuetimes = models.IntegerField(null=True)
    examiner = models.ForeignKey('users.User', null=True, related_name="+")
    examiner_time = models.DateField(null=True)
    examine_statue = models.CharField(max_length=1, default='3')
        # 1 is examining, 2 is examined, 3 is examine failed(or unexamine)
    inblack = models.CharField(max_length=1, default=0)  # 0 is not, 1 is in')
    changewant = models.CharField(max_length=1, default=0)  # 0 is no, 1 is yes
    changereason = models.TextField(null=True)
    changewanttime = models.DateField(null=True)
    certi_num = models.CharField(max_length=100, null=True)
    certi_date = models.CharField(max_length=20, null=True)
    fingrade = models.DateField(null=True)
    three_check = models.CharField(max_length=3, null=True)  # just for me to check whether there is a holder or not

    objects = CompanyManager()


class Suggestion(models.Model):
    connecter = models.CharField(max_length=50)
    content = models.TextField()
    company = models.ForeignKey('Company')


class PeopleInfo(models.Model):
    name = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=2, null=True)
    title = models.CharField(max_length=35, null=True)
    titlemajor = models.CharField(max_length=50, null=True)
    title_file = models.FileField(upload_to="assets/upload_file/title_file/", null=True)  # try and finish
    major = models.CharField(max_length=30, null=True)
    major_file = models.FileField(upload_to="assets/upload_file/major_file/", null=True)  # try and finish
    idnum = models.CharField(max_length=18, null=True, unique=True)
    idnum_file = models.FileField(upload_to="assets/upload_file/idnum_file/", null=True)  # try and finish

    class Meta:
        abstract = True


class StackHolder(PeopleInfo):
    birthd = models.DateField(null=True)
    phone = models.CharField(max_length=16, null=True)
    telephone = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    # train_code = models.CharField(max_length=100, null=True)
    resume = models.TextField(null=True)
    company = models.ForeignKey('Company', related_name='stackholder')
    types = models.CharField(max_length=1, null=True)   # 0, 1, 2
    work_year = models.IntegerField(null=True)   # only for types 1
    work_file = models.FileField(upload_to="assets/upload_file/work_file/", null=True)


class Artisan(PeopleInfo):
    # in many places, i will call it 'people'
    birthd = models.DateField(null=True)
    education = models.CharField(max_length=50, null=True)
    company = models.ForeignKey('Company', related_name='artisan')
    onjob_file = models.FileField(upload_to="assets/upload_file/onjob_file/", null=True)
    jobcerti_file = models.FileField(upload_to="assets/upload_file/jobcerti_file/", null=True)


class Certificate(models.Model):
    num = models.CharField(max_length=100, null=True)
    time = models.DateField(null=True)
    itype = models.CharField(max_length=1, null=True)    # '0', '1'
    file = models.FileField(upload_to="assets/upload_file/certificates_file/", null=True)  # try and finish
    artisan = models.ForeignKey('Artisan', related_name='certificate')


class Project(models.Model):
    name = models.CharField(max_length=100, null=True)
    itype = models.CharField(max_length=10, null=True)
    level = models.CharField(max_length=10, null=True)
    address_a = models.CharField(max_length=50, null=True)
    address_b = models.CharField(max_length=50, null=True)
    address_c = models.CharField(max_length=50, null=True)
    build_company = models.CharField(max_length=100, null=True)
    investment = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    timebef = models.DateField(null=True)
    time = models.DateField(null=True)
    department = models.CharField(max_length=100, null=True)
    approval = models.CharField(max_length=100, null=True, unique=True)
    approval_a_file = models.FileField(upload_to="assets/upload_file/approval_a_file/", null=True)  # try and finish
    approval_b_file = models.FileField(upload_to="assets/upload_file/approval_b_file/", null=True)  # try and finish
    approval_c_file = models.FileField(upload_to="assets/upload_file/approval_c_file/", null=True)  # try and finish
    contract_file = models.FileField(upload_to="assets/upload_file/contract_file/", null=True)
    company = models.ForeignKey('Company', related_name='project')
