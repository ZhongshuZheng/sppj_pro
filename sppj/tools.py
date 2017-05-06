from django.http import StreamingHttpResponse, HttpResponse

from companies.models import Company, StackHolder, Artisan, Project

# #! in this page!

def writelog(request):
    """
    Give a log about what the users has done
    :return:
    """
    pass


def big_file_download(request):
    """
    To download a file after company, by GET method
    :param request:
    :return:
    """
    def file_iterator(file_name, chunk_size=262144):
        with open(file_name, 'rb') as f:    # the 'rb' here is very important!! or you cant get the file
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # for i in request.GET:
    #     print i, '1111'
    if 'FileName' in request.GET and 'explain_template' == request.GET['FileName']:
        the_file_name = "D:/sppj/assets/request_template.doc"  # #!THE TEMP FILE PATH!!!
    elif 'Stackholder' in request.GET:
        # the file is belong to a stackholder
        holder = StackHolder.objects.get(idnum=request.GET['PersonKey'])
        the_file_name = getattr(holder, request.GET['FileName'])
    elif 'Artisan' in request.GET:
        # the file is belong to a Artisan
        holder = Artisan.objects.get(idnum=request.GET['PersonKey'])
        the_file_name = getattr(holder, request.GET['FileName'])
    elif 'Certificate' in request.GET:
        # the file is belong to a Artisan's certificate
        people = Artisan.objects.get(idnum=request.GET['PersonKey'])
        rel_file = people.certificate.get(itype=request.GET['FileType'])
        the_file_name = getattr(rel_file, 'file')
    elif 'Project' in request.GET:
        # the file is belong to a Project
        project = Project.objects.get(approval=request.GET['ProjectKey'])
        the_file_name = getattr(project, request.GET['FileName'])
    else:
        # the file is just belong to a company
        company = Company.objects.get(id=request.GET['CompanyKey'])
        the_file_name = getattr(company, request.GET['FileName'])
    print the_file_name
    if 'FileName' not in request.GET or 'explain_template' != request.GET['FileName']:
        # fpath = "D:/sppj/"+str(the_file_name) # #! if push it in apache
        fpath = the_file_name.path
    else:
        fpath = the_file_name
    response = HttpResponse(file_iterator(fpath), content_type='APPLICATION/OCTET-STREAM')
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
