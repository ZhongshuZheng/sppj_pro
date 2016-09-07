from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView

from sppj.tools import writelog
from users.models import User, MyUserManager

from django.contrib.auth import authenticate, get_user


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
def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            MyUserManager().create_user(signid=form.cleaned_data['signid'],
                                        email=form.cleaned_data['email'],
                                        idnumber=form.cleaned_data['idnumber'],
                                        password=form.cleaned_data['password'],
                                        itype=form.cleaned_data['itype'])
        # else:
        #     # show errors to console:
        #     for i in form.errors:
        #         print i, form.errors[i]
    else:
        form = signupForm()
    writelog(request)  # give the log
    return render_to_response("users/signup.html", {'form': form}, context_instance=RequestContext(request))


@login_required
def detail_message(request, ad_signid=''):
    """
    For users to change the detail message himself or by admin.
    :param request:
    :param ad_signid: The user id I want to look
    :return:
    """
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        form.full_clean()
        if 'email' not in form.errors:
            MyUserManager().change_user(signid=form.data['signid'],
                                        email=form.cleaned_data['email'],
                                        idnumber=form.cleaned_data['idnumber'])
    else:
        if ad_signid == '':
            ad_signid = get_user(request).signid
        form = UserDetailForm(instance=User.objects.get(signid=ad_signid))
    writelog(request)
    return render_to_response('users\detail.html', {'form': form}, context_instance=RequestContext(request))


class UserListView(ListView):
    """
    The view about the list of users for admin.
    """
    model = User
    template_name = 'users\user_list.html'
    context_object_name = "list"    # default = object_list

    def dispatch(self, request, *args, **kwargs):
        # admin required
        if not request.user.is_authenticated() or not request.user.itype == '1':    # ##! change it to 0 !!!!!
            return redirect('index')
        if request.method == 'POST':
            # return to detail_message's get method, and give the id
            ad_signid = request.POST['ad_signid']
            request.method = 'GET'
            return detail_message(request, ad_signid)
        writelog(request)
        return super(UserListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # have nothing else done...
        context = super(UserListView, self).get_context_data(**kwargs)
        return context
