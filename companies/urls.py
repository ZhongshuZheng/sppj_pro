from django.conf.urls import url, include
from companies.views import *


urlpatterns = [
    # for users
    url(r'^info_list/', company_info_list, name='company_info_list'),
    url(r'^info_write/', company_info_write, {'template_name': 'companies/company_info.html'}, name='company_info_write'),
    url(r'^info-papers_write/', company_info_papers_write, {'template_name': 'companies/company_info_paper.html'}, name='company_info_papers_write'),
    url(r'^info-stackholders_write/second/', company_info_stackholders_write, {'page': '1', 'template_name': 'companies/company_info_stackholder.html'},
        name='company_info_stackholders_write2'),
    url(r'^info-stackholders_write/third/', company_info_stackholders_write, {'page': '2', 'template_name': 'companies/company_info_stackholder.html'},
        name='company_info_stackholders_write3'),
    url(r'^info-stackholders_write/', company_info_stackholders_write, {'page': '0', 'template_name': 'companies/company_info_stackholder.html'},
        name='company_info_stackholders_write'),
    url(r'^info-artisans_write/', company_info_peoples_list_write, {'template_name': 'companies/company_people_list.html'}, name='company_info_peoples_write'),
    url(r'^info-artisans_detail_write/', company_info_peoples_detail_write, name='company_info_peoples_detail_write'),
    url(r'^info-projects_write/', company_info_projects_list_write, {'template_name': 'companies/company_project_list.html'}, name='company_info_projects_write'),
    url(r'^info-projects_detail_write/', company_info_projects_detail_write, name='company_info_projects_detail_write'),

    # terrible views because of changeable need
    url(r'^new_write/', company_info_write, {'template_name': 'companies/differentmenu/company_new.html'}, name='company_new_write'),
    url(r'^company_info_write_chg/', company_info_write, {'template_name': 'companies/differentmenu/company_info_chg.html'}, name='company_info_write_chg'),
    url(r'^company_info_papers_write_chg/', company_info_papers_write, {'template_name': 'companies/differentmenu/company_info_paper_chg.html'}, name='company_info_papers_write_chg'),
    # url(r'^company_info_stackholders_write_chg/second/', company_info_stackholders_write, {'page': '1', 'template_name': 'companies/differentmenu/company_info_stackholder_chg.html'},
    #     name='company_info_stackholders_write2'),
    # url(r'^company_info_stackholders_write_chg/third/', company_info_stackholders_write, {'page': '2', 'template_name': 'companies/differentmenu/company_info_stackholder_chg.html'},
    #     name='company_info_stackholders_write3'),
    url(r'^company_info_stackholders_write_chg/', company_info_stackholders_write, {'page': '0', 'template_name': 'companies/differentmenu/company_info_stackholder_chg.html'},
        name='company_info_stackholders_write_chg'),
    url(r'^company_info_peoples_write_chg/', company_info_peoples_list_write, {'template_name': 'companies/differentmenu/company_info_people_list_chg.html'}, name='company_info_peoples_write_chg'),
    # url(r'^company_info_artisans_detail_write_chg/', company_info_peoples_detail_write, {'template_name': 'companies/differentmenu/company_info_people_chg.html'}, name='company_info_artisans_detail_write_chg'),
    url(r'^company_info_projects_write_chg/', company_info_projects_list_write, {'template_name': 'companies/differentmenu/company_info_project_list_chg.html'}, name='company_info_projects_write_chg'),
    # url(r'^company_info_projects_detail_write_chg/', company_info_projects_detail_write, {'template_name': 'companies/differentmenu/company_info_project_chg.html'}, name='company_info_projects_detail_write_chg'),

    # for admin
    url(r'^unex_list/', company_unex_list, name='company_unex_list'),
    url(r'^pub_list/', company_pub_list, name='company_pub_list'),
    url(r'^chg_list/', company_chg_list, name='company_chg_list'),
    url(r'^company_detail/', company_detail, name='company_detail'),
    # some ajax
    url(r'^idnum_repeat_ajax_S/', idnum_repeat_ajaxS),
    url(r'^idnum_repeat_ajax_A/', idnum_repeat_ajaxA),
    url(r'^people_delete_ajax/', people_delete_ajax, name='people_delete_ajax'),
    url(r'^project_delete_ajax/', project_delete_ajax, name='project_delete_ajax'),
    url(r'^company_submit_ajax/', company_submit_ajax, name='company_submit_ajax'),
    url(r'^company_check_ajax/', company_check_ajax, name='company_check_ajax'),
    url(r'^company_change_ajax/', company_change_ajax, name='company_change_ajax'),
    url(r'^company_admin_ajax/', company_admin_ajax, name='company_admin_ajax'),
]
