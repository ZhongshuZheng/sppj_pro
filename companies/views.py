# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, redirect

# Create your views here.
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from companies.models import Company, CompanyManager, StackHolder, Artisan, Certificate, Project
from companies.tools import check_before_submit

from users.models import MyUserManager, User

from sppj.tools import writelog


# forms here:
class CompanyMainInfo(forms.ModelForm):

    # legalpersoncode_file = forms.FileField(required=False)
    examine_statue = forms.FileField(required=False)
    id = forms.CharField(max_length=30, required=False)
    assets = forms.DecimalField(required=False)

    class Meta:
        model = Company
        fields = ['name', 'isgroup', 'phone', 'contacts', 'telephone', 'email', 'fax', 'creditcode',
                  'zipcode', 'zipcodeplace', 'examine_statue', 'itype', 'id', 'assets', 'Company_work_begin',
                  'Company_work_end', 'address_a', 'address_b', 'address_c']
        labels = {
            'name': _('单位名称'.decode("utf8")),
            # 'grade': _('申请级别'.decode("utf8")),
            'address': _('单位固定工作场所'.decode("utf8")),
            'isgroup': _('学会团体会员'.decode("utf8")),
            'phone': _('电话座机'.decode("utf8")),
            'contacts': _('单位联系人'.decode("utf8")),
            'telephone': _('联系人电话'.decode("utf8")),
            'email': _('联系人邮箱'.decode("utf8")),
            'fax': _('联系人QQ号'.decode("utf8")),
            'creditcode': _('统一社会信用代码'.decode("utf8")),
            'zipcodeplace': _('通信地址'.decode("utf8")),
            'zipcode': _('邮编'.decode("utf8")),
            # 'superiordepartment': _('上级主管单位'.decode("utf8")),
            'assets': _('固定资产(单位：万元)'.decode("utf8")),
            # 'capital': _('注册资本或开办资金(单位：万元)'.decode("utf8")),
            'itype': _('单位类型'.decode("utf8")),
        }


class CompanyMainInfoPapers(forms.ModelForm):

    quality_file = forms.FileField(required=False)
    request_file = forms.FileField(required=False)
    explain_file = forms.FileField(required=False)
    system_file = forms.FileField(required=False)
    place_file = forms.FileField(required=False)
    legalpersoncode_file = forms.FileField(required=False)
    id = forms.CharField(max_length=30, required=False)
    examine_statue = forms.FileField(required=False)

    class Meta:
        model = Company
        fields = ['quality_file', 'request_file',
                  'explain_file', 'system_file', 'legalpersoncode_file',
                  'place_file', 'examine_statue', 'id']


class CompanyStackHolders(forms.ModelForm):

    title_file = forms.FileField(required=False)
    major_file = forms.FileField(required=False)
    idnum_file = forms.FileField(required=False)
    work_file = forms.FileField(required=False)
    idnum = forms.CharField(max_length=18, required=False)
    work_year = forms.IntegerField(required=False)

    class Meta:
        model = StackHolder
        fields = ['name', 'sex', 'title', 'title_file', 'major', 'major_file', 'idnum_file', 'phone',
                  'telephone', 'email', 'resume', 'types', 'birthd',
                  'idnum', 'work_year', 'work_file', 'titlemajor']


class CompanyArtisan(forms.ModelForm):

    title_file = forms.FileField(required=False)
    major_file = forms.FileField(required=False)
    idnum_file = forms.FileField(required=False)
    onjob_file = forms.FileField(required=False)
    idnum = forms.CharField(max_length=18, required=False)
    ori_idnum = forms.CharField(max_length=18, required=False)

    file_0 = forms.BooleanField(required=False)
    file_num0 = forms.CharField(max_length=100, required=False)
    file_time0 = forms.DateField(required=False)
    file_itype0 = forms.CharField(max_length=1, required=False)    # 0, 1
    file_file0 = forms.FileField(required=False)

    file_1 = forms.BooleanField(required=False)
    file_num1 = forms.CharField(max_length=100, required=False)
    file_time1 = forms.DateField(required=False)
    file_itype1 = forms.CharField(max_length=1, required=False)    # 0, 1
    file_file1 = forms.FileField(required=False)

    class Meta:
        model = Artisan
        fields = ['name', 'sex', 'birthd', 'title', 'titlemajor', 'title_file', 'major', 'major_file', 'idnum_file',
                  'education', 'idnum', 'onjob_file']


class CertificateForm(forms.ModelForm):
    """
    This form just for the display to the certificate when GET the page. No connect with
    certificate save.
    """

    class Meta:
        model = Certificate
        fields = ['num', 'time', 'file']


class CompanyProject(forms.ModelForm):
    approval_a_file = forms.FileField(required=False)
    approval_b_file = forms.FileField(required=False)
    approval_c_file = forms.FileField(required=False)
    contract_file = forms.FileField(required=False)
    approval = forms.CharField(max_length=100, required=False)
    ori_approval = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Project
        fields = ['name', 'itype', 'level', 'address_a', 'address_b', 'address_c', 'build_company', 'timebef', 'investment',
                  'time', 'approval', 'approval_a_file', 'approval_b_file', 'approval_c_file', 'contract_file', 'department']


# views here:
@login_required
def company_info_list(request):
    # This is not a real list! It just cheat users~~
    # 2016/11/7: now, i subjected an terrible change, this function is NOTHING...
    company = []
    master = get_user(request)
    if master.company:
        company.append(get_user(request).company)
    # These are to record the company which the master is looking at is his own or not
    # if true, the id in his session will be -1
    # else, the id in his session is a company he is looking at, but not his own
    if 'company_ing' not in request.session:
        request.session['company_ing'] = {}
    request.session['company_ing'][get_user(request).signid] = '-1'
    request.session.modified = True
    return render(request, "companies/company_list.html",
                  {'master': master, 'company': company})


@login_required
def company_info_write(request, template_name):
    # Judge if the writer himself:
    # These are to record the company which the master is looking at is his own or not
    # if true, the id in his session will be -1
    # else, the id in his session is a company he is looking at, but not his own
    if 'GET' == request.method and 'notcing' in request.GET:
        if 'company_ing' not in request.session:
            request.session['company_ing'] = {}
        request.session['company_ing'][get_user(request).signid] = '-1'
        request.session.modified = True
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        # I want this view can be at least two mode, one is to create, and one is to update
        mode = 0  # 0 is creat and 1 is update
        base = 'curmb/curmb_self.html'  # the curmb will show in the page, achieve by templates
        company = CompanyMainInfo()
        fileName = '请选择文件！'.decode('utf8')  # the arg for the template to show
        success = 0  # whether the post form is finished, or it just a get request
        if get_user(request).company:
            company = CompanyMainInfo(instance=get_user(request).company)
            fileName = '已存在！'.decode('utf8')
            mode = 1
        if request.method == 'POST':
            company = CompanyMainInfo(request.POST, request.FILES)
            if mode == 0:
                # create a new one
                success = tools_check_filesize(request)
                if success != 3 and company.is_valid():
                    print "valid!"
                    success = 1
                    CompanyManager.page_one_save(company.cleaned_data, get_user(request), new_file=1)
                    fileName = '已存在！'.decode('utf8')
            elif mode == 1:
                # just update the old one
                new_file = 0  # to judge whether the form provides a new file or not
                company.full_clean()
                success = 2
                if len(request.FILES) != 0:
                    new_file = 1
                if len(company.errors) == 0:
                    print "valid!"
                    success = 1
                    CompanyManager.page_one_save(company.cleaned_data, get_user(request), new_file)
                    fileName = '已存在！'.decode('utf8')
                    company = CompanyMainInfo(instance=get_user(request).company)

            print company.errors
        elif 'success' in request.GET:
            success = int(request.GET['success'])
        # for i in company:
        #     print i
    else:
        # i am an admin, give me the power!
        company = CompanyMainInfo(instance=Company.objects.get(
            id=request.session['company_ing'][get_user(request).signid]))
        fileName = "File"
        success = 0
        base = 'curmb/curmb_public.html'
        if Company.objects.get(id=request.session['company_ing'][get_user(request).signid]).examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    writelog(request)
    return render(request, template_name,
                  {'master': get_user(request), 'form': company, 'fileName': fileName,
                   'success': success, 'base': base})


@login_required
def company_info_papers_write(request, template_name):
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        company = CompanyMainInfoPapers(instance=get_user(request).company)
        base = 'curmb/curmb_self.html'
        if not company:
            redirect('company_info_write')
        success = 0                 # whether the post form is finished, or it just a get request
        first_time = 0              # whether it is needed to judge the file must
        ori_c = get_user(request).company.request_file
        if not ori_c:
            # it means that the file has not been already setup, this is the first time.
            first_time = 1
        if request.method == 'POST':
            company = CompanyMainInfoPapers(request.POST, request.FILES)
            success = tools_check_filesize(request)
            if success != 3 and company.is_valid():
                print "valid!"
                success = 1
                first_time = 0
                CompanyManager.page_two_save(company.cleaned_data, get_user(request), request)

            print company.errors
            company = CompanyMainInfoPapers(instance=get_user(request).company)  # this to solve some strange bugs
    else:
        # i am an admin, give me the power!
        company = CompanyMainInfoPapers(instance=Company.objects.get(
            id=request.session['company_ing'][get_user(request).signid]))
        success = 0
        first_time = 0
        base = 'curmb/curmb_public.html'
        if Company.objects.get(id=request.session['company_ing'][get_user(request).signid]).examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    writelog(request)
    return render(request, template_name,
                  {'master': get_user(request), 'form': company,
                   'success': success, 'firtstime': first_time, 'base': base})


@login_required
def company_info_stackholders_write(request, template_name, page='0'):
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        if not get_user(request).company:
            redirect('company_info_write')
        holder = CompanyStackHolders()
        success = 0  # whether the post form is finished, or it just a get request
        first_time = 0  # whether it is needed to judge the file must
        base = 'curmb/curmb_self.html'
        try:
            ori_er = get_user(request).company.stackholder.get(types=page)
        except:
            # it means that the file has not been already setup, this is the first time.
            first_time = 1
        else:
            holder = CompanyStackHolders(instance=ori_er)
        if request.method == 'POST':
            holder = CompanyStackHolders(request.POST, request.FILES)
            holder.full_clean()
            success = tools_check_filesize(request)
            if success != 3 and len(holder.errors) == 0 \
                    or (len(holder.errors) == 1 and 'idnum' in holder.errors and
                                ori_er.idnum == holder.data['idnum']):
                print "valid!"
                success = 1
                first_time = 0
                CompanyManager.page_three_save(holder.cleaned_data, get_user(request),
                                               request, holder.data['idnum'])
                holder = CompanyStackHolders(instance=StackHolder.objects.get(idnum=holder.data['idnum']))

            print holder.errors
        examine_statue = get_user(request).company.examine_statue
    else:
        # i am an admin, give me the power!
        holder = CompanyStackHolders()
        try:
            holder = CompanyStackHolders(instance=Company.objects.get(
                id=request.session['company_ing'][get_user(request).signid]).stackholder.get(types=page))
        except:
            pass
        success = 0
        first_time = 0
        examine_statue = Company.objects.get(id=request.session['company_ing'][get_user(request).
                                     signid]).examine_statue
        base = 'curmb/curmb_public.html'
        if examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    writelog(request)
    return render(request, template_name,
                  {'master': get_user(request), 'form': holder, 'success': success,
                   'page': page, 'firtstime': first_time, 'examine_statue': examine_statue,
                   'base': base})


@login_required
def company_info_peoples_list_write(request, template_name):
    if request.method == 'POST':
        request.method = 'GET'
        return company_info_peoples_detail_write(request, request.POST['a_idnum'])
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        company = get_user(request).company
        artisan = company.artisan.all()
        base = 'curmb/curmb_self.html'
    else:
        # i am an admin, give me the power!
        company = Company.objects.get(id=request.session['company_ing'][get_user(request).signid])
        artisan = company.artisan.all()
        base = 'curmb/curmb_public.html'
        if company.examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    return render(request, template_name,
                  {'master': get_user(request), 'list': artisan, 'company': company, 'base': base})


@login_required
def company_info_peoples_detail_write(request, a_idnum='0'):
    """
    To find or post the people's detail message
    The same time find or post the certificate of the artisan
    :param request:
    :param a_idnum: the idnum of the people if he exists. Ensure 0 can't be in the database!!!
    :return:
    """
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        if not get_user(request).company:
            redirect('company_info_write')
        people = CompanyArtisan()
        f0 = CertificateForm()
        f1 = CertificateForm()
        base = 'curmb/curmb_self.html'
        success = 0  # whether the post form is finished, or it just a get request
        first_time = 0  # whether it is needed to judge the file must
        ori_er = False  # check if it is edit or create. if edit, it will be the origin
        company_examine_statue = '3'  # the company's examine_statue, if 1, the page can't be change
        try:
            if request.method == 'GET':
                ori_er = Artisan.objects.get(idnum=a_idnum)
                company_examine_statue = ori_er.company.examine_statue
            else:
                ori_er = Artisan.objects.get(idnum=request.POST['ori_idnum'])
        except:
            # it means that the file has not been already setup, this is the first time.
            first_time = 1
        else:
            people = CompanyArtisan(instance=ori_er)
            try:
                f0 = CertificateForm(instance=ori_er.certificate.get(itype=0))
            except:
                pass
            try:
                f1 = CertificateForm(instance=ori_er.certificate.get(itype=1))
            except:
                pass
        if request.method == 'POST':
            people = CompanyArtisan(request.POST, request.FILES)
            people.full_clean()
            success = 2
            print people.errors
            success = tools_check_filesize(request)
            if success != 3 and len(people.errors) == 0 \
                    or (len(people.errors) == 1 and 'idnum' in people.errors and
                                ori_er and ori_er.idnum == people.data['idnum']):
                print "valid!"
                success = 1
                first_time = 0
                CompanyManager.page_four_save(people.cleaned_data, get_user(request),
                                              request, people.data['idnum'], request.POST['ori_idnum'])
                ori_idnum = people.data['idnum']
                people = CompanyArtisan(instance=Artisan.objects.get(idnum=ori_idnum))
                try:
                    f0 = CertificateForm(instance=Artisan.objects.get(idnum=ori_idnum).certificate.get(itype=0))
                except:
                    f0 = CertificateForm()
                try:
                    f1 = CertificateForm(instance=Artisan.objects.get(idnum=ori_idnum).certificate.get(itype=1))
                except:
                    f1 = CertificateForm()
    else:
        # i am an admin, give me the power!
        ori_er = Artisan.objects.get(idnum=a_idnum)
        people = CompanyArtisan(instance=ori_er)
        f0 = CertificateForm()
        f1 = f0
        try:
            f0 = CertificateForm(instance=ori_er.certificate.get(itype=0))
        except:
            pass
        try:
            f1 = CertificateForm(instance=ori_er.certificate.get(itype=1))
        except:
            pass
        success = 0
        first_time = 0
        company_examine_statue = Company.objects.get(id=request.session['company_ing'][get_user(request).signid]).examine_statue
        base = 'curmb/curmb_public.html'
        if company_examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    writelog(request)
    return render(request, "companies/company_info_people.html",
                  {'master': get_user(request), 'form': people, 'f0': f0, 'f1': f1, 'success': success,
                   'firtstime': first_time, "examine_statue": company_examine_statue, 'base': base})


def company_info_projects_list_write(request, template_name):
    if request.method == 'POST':
        request.method = 'GET'
        return company_info_projects_detail_write(request, request.POST['a_approval'])
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        company = get_user(request).company
        projects = company.project.all()
        base = 'curmb/curmb_self.html'
    else:
        # i am an admin, give me the power!
        company = Company.objects.get(id=request.session['company_ing'][get_user(request).signid])
        projects = company.project.all()
        base = 'curmb/curmb_public.html'
        if company.examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    return render(request, template_name,
                  {'master': get_user(request), 'list': projects, 'company': company, 'base': base})


def company_info_projects_detail_write(request, a_approval='0'):
    """
    Mainly copy from "company_info_peoples_detail_write"
    :param request:
    :param a_approval: the approval of the people if he exists. Ensure 0 can't be in the database!!!
    :return:
    """
    # Judge the admin or not first:
    if request.session['company_ing'][get_user(request).signid] == '-1':
        if not get_user(request).company:
            redirect('company_info_write')
        project = CompanyProject()
        base = 'curmb/curmb_self.html'
        success = 0  # whether the post form is finished, or it just a get request
        first_time = 0  # whether it is needed to judge the file must
        ori_er = False  # check if it is edit or create. if edit, it will be the origin
        company_examine_statue = '3'  # the company's examine_statue, if 1, the page can't be change
        try:
            if request.method == 'GET':
                ori_er = Project.objects.get(approval=a_approval)
                company_examine_statue = ori_er.company.examine_statue
            else:
                ori_er = Project.objects.get(approval=request.POST['ori_approval'])
        except:
            # it means that the file has not been already setup, this is the first time.
            first_time = 1
        else:
            project = CompanyProject(instance=ori_er)
        if request.method == 'POST':
            project = CompanyProject(request.POST, request.FILES)
            project.full_clean()
            success = 2
            print project.errors
            success = tools_check_filesize(request)
            if success != 3 and len(project.errors) == 0 \
                    or (len(project.errors) == 1 and 'approval' in project.errors and
                                ori_er and ori_er.approval == project.data['approval']):
                print "valid!"
                success = 1
                first_time = 0
                CompanyManager.page_five_save(project.cleaned_data, get_user(request),
                                              request, project.data['approval'], request.POST['ori_approval'])
                project = CompanyProject(instance=Project.objects.get(approval=project.data['approval']))
    else:
        # i am an admin, give me the power!
        project = CompanyProject(instance=Project.objects.get(approval=a_approval))
        success = 0
        first_time = 0
        company_examine_statue = Company.objects.get(id=request.session['company_ing'][get_user(request)
                                                     .signid]).examine_statue
        base = 'curmb/curmb_public.html'
        if company_examine_statue == '1':
            base = 'curmb/curmb_unex.html'
    writelog(request)
    return render(request, "companies/company_info_project.html",
                  {'master': get_user(request), 'form': project, 'success': success,
                   'firtstime': first_time, "examine_statue": company_examine_statue, 'base':base})


# views for admin
@login_required
def company_detail(request):
    # some is admin, some is visiter want to visit others.
    if 'company_ing' not in request.session:
        request.session['company_ing'] = {}
    request.session['company_ing'][get_user(request).signid] = request.POST['c_id']
    request.session.modified = True 
    return company_info_write(request, template_name='companies/company_info.html')


@login_required
def company_unex_list(request):
    company = Company.objects.filter(examine_statue='1')
    return render(request, "companies/company_list_ad.html",
                  {'master': get_user(request), 'company': company, 'page': 1})


@login_required
def company_pub_list(request):
    company = Company.objects.filter(examine_statue='2')
    return render(request, "companies/company_list_ad.html",
                  {'master': get_user(request), 'company': company, 'page': 2})


@login_required
def company_chg_list(request):
    company = Company.objects.filter(changewant='1')
    return render(request, "companies/company_list_ad.html",
                  {'master': get_user(request), 'company': company, 'page': 3})


# ajax
def idnum_repeat_ajaxS(request):
    # the ajax view for weather stackholder repeat or not
    fieldValue = request.GET['fieldValue']
    fieldId = request.GET['fieldId']

    if StackHolder.objects.filter(idnum=fieldValue):
        no_repeat = False
    else:
        no_repeat = True
    results = [fieldId, no_repeat]
    return JsonResponse(results, safe=False)


def idnum_repeat_ajaxA(request):
    # the ajax view for weather artisan repeat or not
    fieldValue = request.GET['fieldValue']
    fieldId = request.GET['fieldId']

    if Artisan.objects.filter(idnum=fieldValue):
        no_repeat = False
    else:
        no_repeat = True
    results = [fieldId, no_repeat]
    return JsonResponse(results, safe=False)


def people_delete_ajax(request):
    if not request.user.is_authenticated():
        return redirect('index')

    CompanyManager.delete_aritsan(request.GET['del_id'])
    return JsonResponse({}, safe=False)


def project_delete_ajax(request):
    if not request.user.is_authenticated():
        return redirect('index')

    CompanyManager.delete_project(request.GET['del_id'])
    return JsonResponse({}, safe=False)


def company_submit_ajax(request):
    if not request.user.is_authenticated():
        return redirect('index')
    c = get_user(request).company
    c.score = 60
    c.examine_statue = '1'    # changed to examining
    c.save()
    return JsonResponse({}, safe=False)


def company_check_ajax(request):
    # to check 60 score or less.
    if not request.user.is_authenticated():
        return redirect('index')
    ans = check_before_submit(request)
    if ans == 1:
        return JsonResponse(ans, safe=False)
    return JsonResponse(ans.encode('utf8'), safe=False)


def company_change_ajax(request):
    if not request.user.is_authenticated():
        return redirect('index')

    c = User.objects.get(signid=request.GET['sub_id']).company
    c.changewant = '1'    # changed to examining
    c.changewanttime = datetime.date.today()
    c.save()
    return JsonResponse({}, safe=False)


def company_admin_ajax(request):
    if not request.user.is_authenticated():
        return redirect('index')
    action = request.GET['page']
    c = Company.objects.get(id=request.GET['sub_id'])
    if action == '1':
        c.examine_statue = '2'    # changed to examined
    elif action == '2':
        c.examine_statue = '3'    # changed to unexamined
    elif action == '3':
        c.changewant = '0'
        c.examine_statue = '3'    # changed to unexamined
        c.changereason = ''
    elif action == '4':
        c.changewant = '0'    # changed to examined
        c.changereason = ''
    c.save()
    return JsonResponse({}, safe=False)


def tools_check_filesize(request):
    """
    To check if the file uploaded too much to save
    :param request:
    :return:
    """
    success = 2
    #for j in request.FILES:
    #    if j.size() > 100000000:
    #        success = 3
    return success
