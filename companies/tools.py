# -*- coding:utf-8 -*-
from django.contrib.auth import get_user

from companies.models import Company, StackHolder, Artisan, Project

# #! in this page

# the methods about the submit 60 score
def check_before_submit(request):
    """
    To check whether the company can get 60 score and submit itself.
    :param request:
    :return: '1' if all passed, error message if failed.
    """
    message = ""
    try:
        company = get_user(request).company

        # stackholder:
        stackholder = company.stackholder.get(types=1)
        if stackholder.work_year <= 5:
            message += "技术负责人必须具有5年以上从事水土保持工作的经历;".decode("utf8")

        if stackholder.major == "非上述专业".decode('utf8') or stackholder.title == "助工".decode("utf8") \
                or stackholder.title == "工程师".decode("utf8"):
            message += "技术负责人必须具有水土保持或水土保持相关专业的高级专业技术职称;".decode("utf8")

        # artisan
        artisan = company.artisan.exclude(major="非上述类别")
        if len(artisan) < 3:    # #! 10
            message += "具有水土保持（或相关专业）大专以上学历、技术职称或从业经历的专业技术人员不可少于10人;".decode("utf8")
            return message

        atr_sum = len(artisan.filter(title="高级工程师")) + len(artisan.filter(title="教授"))
        for i in artisan.filter(title="工程师"):
            try:
                i.certificate.get(itype=1)
                atr_sum += 1
            except:
                pass
        for i in artisan.filter(title="助理工程师"):
            try:
                i.certificate.get(itype=1)
                atr_sum += 1
            except:
                pass
        if atr_sum < 2:
            message += "高级以上专业技术职称人员或注册水利水电工程水土保持工程师不少于2人;".decode("utf8")
            return message

        if len(artisan.exclude(title="助理工程师")) < 4:
            message += "中级以上专业技术职称人员不得少于4 人;".decode("utf8")
            return message

        if len(artisan.filter(major="水土保持类")) < 2:
            message += "所学专业为水土保持的人员不少于2人;".decode("utf8")
            return message

        atr_sum = len(artisan.filter(major="水利工程类")) + len(artisan.filter(major="其他土木工程类"))
        if atr_sum < 1:
            message += "所学专业为水利工程类或其他土木工程类的人员不得少于1人;".decode("utf8")
            return message
    except:
        return '申请提交信息不完整，请核对申请需求基本材料。'.decode('utf8')
    print 'ans', message
    if message == "":
        return 1
    return message
