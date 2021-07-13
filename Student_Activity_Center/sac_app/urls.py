from django.conf.urls import url
from django.urls import path

from sac_app import views

app_name = "sac_app"

urlpatterns = [
    # 1 登录 ----- （封正泽）----- %
    path('login/', views.login, name="login"),
    # 1 验证码 ----- （赵碧）----- %
    path('check_code/', views.check_code),
    # 1 注册 ----- （封正泽）----- %
    path('login/register/', views.register, name="register"),
    # 1 激活 ----- （封正泽）----- %
    path('active/', views.stu_active, name='active'),
    # 1 忘记密码 ----- （李渊科）----- %
    path('login/forgetpwd/', views.forgetpwd, name="forgetpwd"),
    # 1 修改密码 ----- （李渊科）----- %
    path('login/changepwd', views.changepwd, name="changepwd"),
    # 学生:主页 ~~~~~
    path('stu_home', views.stu_home, name="stu_home"),
    # 2 学生: 活动大厅 ----- (袁丰) ~~~~~
    path('stu_home/stu_activity', views.stu_activity, name="stu_activity"),
    # 2 学生：已参加活动页 ----- (袁丰) ~~~~~
    path('stu_home/stu_join_activity/', views.stu_join_activity, name="stu_join_activity"),
    # 1 学生：创建队伍 ----- (李渊科) ~~~~~
    path('stu_home/stu_create_team/', views.stu_createteam, name="stu_create_team"),
    # 1 2 学生：我的队伍 ~~~~~ 1
    path('stu_home/stu_my_team/', views.stu_myteam, name="stu_my_team"),
    # 1 2 学生：其他队伍 ~~~~~ 1
    path('stu_home/stu_other_team/', views.stu_otherteam, name="stu_other_team"),
    # 2 学生：个人中心 ~~~~ 2
    path('stu_home/stu_center/', views.stu_center, name="stu_center"),
    # 1 2学生：修改个人信息 ----- (覃智科)  ~~~~~
    path('stu_home/stu_modify_message/', views.stu_modify_message, name='stu_modify_message'),
    # 2 学生：公告页 ~~~~ 2
    path('stu_home/stu_notice/', views.stu_notice, name="stu_notice"),
    # 2 学生：进入活动公告 ~~~~ 2
    path('stu_home/stu_notice/stu_notice_act/', views.stu_notice_act, name="stu_notice_act"),
    # 2 学生：进入系统公告 ~~~~ 2
    path('stu_home/stu_notice/stu_notice_sys/', views.stu_notice_sys, name="stu_notice_sys"),


    # 组织者 ：主页  ~~~~~
    path('org_home/', views.org_home, name="org_home"),
    # 1 组织者 ：发布活动 ----- (覃智科) ~~~~~
    path('org_home/org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 1 组织者：发布公告 ----- (覃智科) ~~~~~
    path('org_home/org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 2 组织者：公告页  ~~~~ 2
    path('org_home/org_notice/', views.org_notice, name="org_notice"),
    # 2 组织者：查看已发活动 -----（秦浩廷）~~~~~
    path('org_home/org_view_posted_activity/', views.org_view_posted_activity, name="org_view_posted_activity"),
    # 1 2 组织者：修改活动 ~~~~ 1
    path('org_home/org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 2 组织者中心 ~~~~ 2
    path('org_home/org_center/', views.org_center, name="org_center"),
    # 1 2 组织者：修改组织者信息 ~~~~ 1
    path('org_home/org_modify_message/', views.org_modify_message, name="org_modify_message"),


    # 管理者： 主页 ~~~~
    path('mag_home/', views.mag_home, name="mag_home"),
    # 2 管理者：审核列表页 ~~~~ 2
    path('mag_home/mag_examine/', views.mag_examine, name="mag_examine"),
    # 1 2 管理者：审核 ~~~~ 1
    path('mag_home/mag_examine_details/', views.mag_examine_details, name="mag_examine_details"),
    # 1 2 管理者：管理组织者（增删查） ~~~~ 1
    path('mag_home/mag_manage/', views.mag_manage, name="mag_manage"),
    # 2 管理者：公告 ~~~~ 2
    path('mag_home/mag_notice/', views.mag_notice, name="mag_notice"),
    # 1 管理者：发布系统公告 ~~~~ 1
    path('mag_home/mag_launch_notice/', views.mag_launch_notice, name="mag_launch_notice"),
    # 2 管理者：进入活动公告的 ~~~~ 2
    path('mag_home/mag_home/mag_notice/mag_notice_act/', views.mag_notice_act, name="mag_notice_act"),
    # 2 管理者：进入系统公告的 ~~~~ 2
    path('mag_home/mag_notice/mag_notice_sys/', views.mag_notice_sys, name="mag_notice_sys"),

]
