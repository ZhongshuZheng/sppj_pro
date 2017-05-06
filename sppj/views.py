from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from sppj.tools import big_file_download


@login_required
def index(request):
    return render(request, "index.html", {'master': get_user(request)})


@login_required
def download_view(request):
    return big_file_download(request)
