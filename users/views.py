# "##!" is need to be rewrite!!!
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView

from sppj.tools import writelog
from users.models import User, MyUserManager

from django.contrib.auth import authenticate, get_user, login, logout


# forms here:
class signupForm(forms.ModelForm):

    password_repeat = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['signid', 'password', 'email', 'idnumber', 'itype']



class UserDetailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['signid', 'idnumber', 'email']


# views here:
def user_login(request):
    # logout(request)
    error = '0'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(signid=username, password=password)
        if user is not None and not User.objects.get(signid=username).itype == '2':
            login(request, user)
            writelog(request)
            return render(request, 'index.html', {'master': get_user(request)})
        error = '1'
    writelog(request)
    return render(request, 'users/login.html', {"error": error})


def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            MyUserManager().create_user(signid=form.cleaned_data['signid'],
                                        email=form.cleaned_data['email'],
                                        idnumber=form.cleaned_data['idnumber'],
                                        password=form.cleaned_data['password'],
                                        itype=form.cleaned_data['itype'])
            user = authenticate(signid=form.cleaned_data['signid'], password=form.cleaned_data['password'])
            login(request, user)
            writelog(request)
            return render(request, "index.html", {'master': get_user(request)})
        # else:
        #     # show errors to console:
        #     for i in form.errors:
        #         print i, form.errors[i]
    else:
        form = signupForm()
    writelog(request)  # give the log
    return render(request, "users/login.html", {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'users/login.html',{})


@login_required
def detail_message(request, ad_signid=''):
    """
    For users to change the detail message himself or by admin.
    :param request:
    :param ad_signid: The user id I want to look
    :return:
    """
    success = '0'
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        form.full_clean()
        if 'email' not in form.errors and 'idnumber' not in form.errors:
            MyUserManager().change_user(signid=form.data['signid'],
                                        email=form.cleaned_data['email'],
                                        idnumber=form.cleaned_data['idnumber'])
            success = '1'
    else:
        if ad_signid == '':
            ad_signid = get_user(request).signid
        form = UserDetailForm(instance=User.objects.get(signid=ad_signid))
    writelog(request)
    return render(request, 'users/detail.html', {'master': get_user(request), 'form': form, 'success': success})


@login_required
def change_code(request):
    success = '0'
    if request.method == 'POST':
        success = '2'
        username = get_user(request).signid
        password = request.POST['ori_password']
        user = authenticate(signid=username, password=password)
        if user is not None:
            success = '1'
            user.set_password(request.POST['new_pw'])
            user.save()
            user = authenticate(signid=username, password=request.POST['new_pw'])
            login(request, user)
    writelog(request)
    return render(request, 'users/changecode.html', {'master': get_user(request), 'success': success})


# class UserListView(ListView):
#     """
#     The view about the list of users for admin.
#     It is too struggle!!!!
#     """
#     model = User
#     tempplate_name = 'users\user_list.html'
#     context_object_name = "list"    # default = object_list
#
#     def dispatch(self, request, *args, **kwargs):
#         # admin required
#         if not request.user.is_authenticated() or not request.user.itype == '0':    # ##! change it to 0 !!!!!
#             return redirect('index')
#         if request.method == 'POST':
#             # return to detail_message's get method, and give the id
#             ad_signid = request.POST['ad_signid']
#             request.method = 'GET'
#             return detail_message(request, ad_signid)
#         writelog(request)
#         return super(UserListView, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         # have nothing else done...
#         context = super(UserListView, self).get_context_data(**kwargs)
#         context['list'] = User.objects.filter(itype='1')
#         return context


def user_list(request):
    # admin required
    if not request.user.is_authenticated() or not request.user.itype == '0':    # ##! change it to 0 !!!!!
        return redirect('index')
    if request.method == 'POST':
        # return to detail_message's get method, and give the id
        ad_signid = request.POST['ad_signid']
        request.method = 'GET'
        return detail_message(request, ad_signid)
    list = User.objects.filter(itype='1')
    writelog(request)
    return render(request, 'users/user_list.html', {'master': get_user(request), 'list': list})


# ajax
def user_repeat_ajax(request):
    # the ajax view for weather user repeat or not
    fieldValue = request.GET['fieldValue']
    fieldId = request.GET['fieldId']

    if User.objects.filter(signid=fieldValue):
        no_repeat = False
    else:
        no_repeat = True
    results = [fieldId, no_repeat]
    return JsonResponse(results, safe=False)


def user_delete_ajax(request):
    # the ajax view for weather user repeat or not
    if not request.user.is_authenticated() or not request.user.itype == '1':  # ##! change it to 0 !!!!!
        return redirect('index')

    user = User.objects.get(signid=request.GET['del_id'])
    user.itype = '2'
    user.save()
    return JsonResponse({}, safe=False)
