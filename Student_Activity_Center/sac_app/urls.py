# coding=utf-8
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from sac_app import views

app_name = "sac_app"
urlpatterns = [
    # path('', admin.site.urls),
    # 1 登录
    path('login/', views.login),
    # 验证码
    path('check_code/', views.check_code),
    # 1 注册
    path('login/register/', views.register),
    # 1 激活
    path('active/',views.stu_active),
    # 1 忘记密码
    path('login/forgetpwd/', views.forgetpwd),
    # 学生:主页
    path('stu_home/', views.stu_home),
    # 2学生: 活动大厅
    path('stu_home/stu_activity/', views.stu_activity),
    # 2 学生：已参加活动页
    path('stu_home/stu_join_activity/', views.stu_join_activity),
    # 1 2 学生：个人中心  (覃智科)
    path('stu_home/stu_center/', views.stu_center, name="stu_center"),
    # 2 1学生：活动详情页 ~ 2
    path('stu_home/stu_activity_details/', views.stu_activity_details, name="stu_activity_details"),
    # 2 学生：活动列表页  - （秦浩廷）
    path('stu_home/stu_activity_list/', views.stu_activity_list, name="stu_activity_list"),
    # 1 学生：创建队伍
    path('stu_home/stu_createteam/', views.stu_createteam, name="stu_create_team"),
    # 1 2 学生：我的所有队伍 ~ 2
    path('stu_home/stu_myteam/', views.stu_myteam, name="stu_my_team"),
    # 1 2 学生：具体活动的全部队伍 ~ 2
    path('stu_home/stu_otherteam/', views.stu_otherteam, name="stu_other_team"),


    # 组织者 ：主页
    path('org_home/', views.org_home, name="org_home"),
    # 1组织者 ：发布活动
    path('org_home/org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 1组织者：发布公告
    path('org_home/org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 1 2组织者：修改活动  ~1
    path('org_home/org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 2 组织者查看特定活动详情
    path('org_home/org_activity_details/', views.org_activity_details, name="org_activity_details"),
    # 2 组织者：查看已发活动 - （秦浩廷）
    path('org_home/org_view_posted_activity/', views.org_view_posted_activity, name="org_view_pasted_activity"),


    # 管理者： 主页
    path('mag_home/', views.mag_home, name="mag_home"),
    # 1 2管理者：审核列表页  ~1
    path('mag_home/mag_examine_list/', views.mag_examine_list, name="mag_examine_list"),
    # 2 管理者：审核详情页
    path('mag_home/mag_details',views.mag_details,name="mag_details"),
    # 1 2管理者：管理组织者  ~1
    path('mag_home/mag_manage/', views.mag_manage, name="mag_manage"),

    # 2 公告：公告主页
    path('notice/', views.notice, name="notice"),
    # 2 公告：活动公告
    path('notice/notice_activity/', views.notice_activity, name="notice_activity"),
    # 2 公告：系统公告
    path('notice/notice_sys/', views.notice_sys, name="notice_sys"),
]