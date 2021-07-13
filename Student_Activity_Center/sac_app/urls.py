from django.conf.urls import url
from django.urls import path

from sac_app import views

app_name = "sac_app"

urlpatterns = [
    # 登录
    path('login/', views.login, name="login"),
    # 验证码
    path('check_code/', views.check_code),
    # 注册
    path('login/register/', views.register, name="register"),
    # 忘记密码
    path('login/forgetpwd/', views.forgetpwd, name="forgetpwd"),


    # 学生：首页
    path('stu_home', views.stu_home, name="stu_home"),
    # 学生:活动大厅
    path('stu_home/stu_activity', views.stu_activity, name="stu_activity"),
    # 学生：已参加活动页
    path('stu_home/stu_join_activity/', views.stu_join_activity, name="stu_join_activity"),
    # 学生：创建队伍
    path('stu_home/stu_create_team/', views.stu_createteam, name="stu_create_team"),
    # 学生：我的队伍
    path('stu_home/stu_my_team/', views.stu_myteam, name="stu_my_team"),
    # 学生：其他队伍
    path('stu_home/stu_other_team/', views.stu_otherteam, name="stu_other_team"),
    # 学生：个人中心
    path('stu_home/stu_center/', views.stu_center, name="stu_center"),
    # 学生：修改个人信息 ~~~~
    path('stu_home/stu_modify_message/', views.stu_modify_message, name='stu_modify_message'),
    # 学生：公告页
    path('stu_home/stu_notice/', views.stu_notice, name="stu_notice"),
    # 学生：进入活动公告
    path('stu_home/stu_notice/stu_notice_act/', views.stu_notice_act, name="stu_notice_act"),
    # 学生：进入系统公告
    path('stu_home/stu_notice/stu_notice_sys/', views.stu_notice_sys, name="stu_notice_sys"),


    # 组织者 ：主页
    path('org_home/', views.org_home, name="org_home"),
    # 组织者 ：发布活动
    path('org_home/org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 组织者：发布公告
    path('org_home/org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 组织者：公告页
    path('org_home/org_notice/', views.org_notice, name="org_notice"),
    # 组织者：修改活动
    path('org_home/org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 组织者：查看已发活动
    path('org_home/org_view_pasted_activity/', views.org_view_posted_activity, name="org_view_pasted_activity"),
    # 组织者中心  ~~~
    path('org_home/org_center/', views.org_center, name="org_center"),
    # 组织者：修改组织者信息
    path('org_home/org_modify_message/', views.org_modify_message, name="org_modify_message"),


    # 管理者： 主页
    path('mag_home/', views.mag_home, name="mag_home"),
    # 管理者：审核
    path('mag_home/mag_examine/', views.mag_examine, name="mag_examine"),
    # 管理者：管理组织者
    path('mag_home/mag_manage/', views.mag_manage, name="mag_manage"),
    # 管理者：公告
    path('mag_home/mag_notice/', views.mag_notice, name="mag_notice"),
    # 管理者：发布系统公告
    path('mag_home/mag_launch_notice/', views.mag_launch_notice, name="mag_launch_notice"),
    # 管理者：进入活动公告的
    path('mag_home/mag_home/mag_notice/mag_notice_act/', views.mag_notice_act, name="mag_notice_act"),
    # 管理者：进入系统公告的
    path('mag_home/mag_notice/mag_notice_sys/', views.mag_notice_sys, name="mag_notice_sys"),

]
