# coding=utf-8
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path('', admin.site.urls),

    path('login/', views.login),  #登录    1
    path('check_code/', views.check_code), #验证码
    path('login/register/', views.register), #注册     1
    path('login/forgetpwd/', views.forgetpwd), #忘记密码     1


    # 学生:主页
    path('stu_home/', views.stu_home),
    # 2学生:活动大厅       2
    path('stu_home/stu_activity/', views.stu_activity),
    # 2学生：已参加活动页   2
    path('stu_home/stu_join_activity/', views.stu_join_activity),
    # 1 2学生：个人中心
    path('stu_home/stu_center/', views.stu_center, name="stu_center"),
    # 2 1学生：可参加活动页
    path('stu_home/stu_activity_yes/', views.stu_activity_yes, name="stu_activity_yes"),
    #2 学生：不可参加活动
    path('stu_home/stu_activity_no/', views.stu_activity_no, name="stu_activity_no"),
    #1 学生：创建队伍
    path('stu_home/stu_createteam/', views.stu_createteam, name="stu_create_team"),
    #1 2 学生：我的队伍
    path('stu_home/stu_myteam/', views.stu_myteam, name="stu_my_team"),
    #1 2学生：其他队伍
    path('stu_home/stu_otherteam/', views.stu_otherteam, name="stu_other_team"),



    # 组织者 ：主页
    path('org_home/', views.org_home, name="org_home"),
    # 1组织者 ：发布活动
    path('org_home/org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 1组织者：发布公告
    path('org_home/org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    #1 2组织者：修改活动
    path('org_home/org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    #2 组织者：查看已发活动
    path('org_home/org_view_pasted_activity/', views.org_view_pasted_activity, name="org_view_pasted_activity"),


    # 管理者： 主页
    path('mag_home/', views.mag_home, name="mag_home"),
    # 12管理者：审核
    path('mag_home/mag_examine/', views.mag_examine, name="mag_examine"),
    # 12管理者：管理组织者
    path('mag_home/mag_manage/', views.mag_manage, name="mag_manage"),


    # 2 公告：公告主页
    path('notice/', views.notice, name="notice"),
    # 2 公告：活动公告
    path('notice/notice_activity/', views.notice_activity, name="notice_activity"),
    # 2 公告：系统公告
    path('notice/notice_sys/', views.notice_sys, name="notice_sys"),
]