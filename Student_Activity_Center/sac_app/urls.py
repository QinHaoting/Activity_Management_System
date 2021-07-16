from django.conf.urls import url
from django.urls import path, re_path

from sac_app import views

app_name = "sac_app"

urlpatterns = [

    # 1 登录 ----- （封正泽）----- (秦浩廷)
    url('^login/', views.login, name="login"),
    # 注销
    path('logout/', views.logout, name='logout'),
    # 1 验证码 ----- （赵碧）----- （秦浩廷）
    path('check_code/', views.check_code),
    # 1 注册 ----- （封正泽）----- （秦浩廷）
    path('login/register/', views.register, name="register"),
    # 1 激活 ----- （封正泽）----- （秦浩廷）
    path('active/', views.stu_active, name='active'),
    # 1 忘记密码 ----- （李渊科）----- （秦浩廷）
    path('login/forgetpwd/', views.forgetpwd, name="forgetpwd"),
    # 1 修改密码 ----- （李渊科）----- （秦浩廷）
    path('changepwd/', views.changepwd, name="changepwd"),

    # 学生:主页 ~~~~~
    path('stu_home', views.stu_home, name="stu_home"),
    path('stu_home/stu_join_otherteam/', views.act_join_other_team, name="act_join_other_team"),
    # 2 学生: 活动大厅 ----- (秦浩廷) ~~~~~
    path('stu_home/stu_activity/', views.stu_activity, name="stu_activity"),
    # 2 学生：活动详情页 ~~~~~
    re_path(r'^stu_home/stu_activity/stu_activity_details/(\d+)', views.stu_activity_details,
            name="stu_activity_details"),
    # 2 学生：已参加活动页 ----- (袁丰) ~~~~~
    path('stu_home/stu_join_activity/', views.stu_join_activity, name="stu_join_activity"),
    # 学生：已参加活动详情页
    re_path(r'^stu_home/stu_join_activity/stu_join_activity_details/(\d+)', views.stu_join_activity_details,
            name="stu_join_activity_details"),
    # 1 学生：创建队伍 ----- (李渊科) ~~~~~
    # re_path(r'^stu_home/stu_create_team/(\d+)', views.stu_create_team, name="stu_create_team"),
    path('stu_home/stu_create_team/', views.stu_create_team, name="stu_create_team"),
    # 1 2 学生：我的队伍 ~~~~~ 2
    path('stu_home/stu_myteam/', views.stu_myteam, name="stu_myteam"),
    re_path(r'^stu_home/stu_activity/stu_activity_details/stu_view_myteam/(\d+)', views.stu_view_myteam,
            name="stu_view_myteam"),
    re_path(r'^stu_home/stu_join_activity/stu_join_activity_details/stu_view_myteam/(\d+)',
            views.stu_view_myteam, name="stu_view_myteam"),
    re_path(r'^stu_home/stu_myteam/stu_view_myteam/(\d+)', views.stu_view_myteam, ),
    # 1 2 学生：其他队伍 ~~~~~ 1
    re_path(r'^stu_home/stu_activity/stu_activity_details/stu_join_other_team/(\d+)', views.act_join_other_team,
            name="stu_join_other_team"),
    re_path(
        r'^sac_app/stu_home/stu_join_activity/stu_join_activity_details/stu_join_other_team/stu_view_other_team/(\d+)',
        views.stu_view_other_team, name="stu_view_other_team"),

    re_path(r'^stu_home/stu_join_activity/stu_join_activity_details/stu_join_other_team/(\d+)',
            views.act_join_other_team,
            name="stu_join_other_team"),
    re_path(r'^stu_home/stu_join_activity/stu_join_activity_details/stu_join_other_team/stu_view_other_team/(\d+)',
            views.stu_view_other_team, name="stu_view_other_team"),
    # 学生：查看其它队伍
    re_path(r'^stu_home/stu_activity/stu_activity_details/stu_join_other_team/stu_view_other_team/(\d+)',
            views.stu_view_other_team, name="stu_view_other_team"),
    # 2 学生：个人中心 ~~~~ 2
    path('stu_home/stu_center/', views.stu_center, name="stu_center"),
    # 1 2学生：修改个人信息 ----- (覃智科)  ~~~~~
    # re_path(r'^stu_home/stu_activity/stu_activity_details/stu_join_other_team/(\d+)', views.stu_modify_message,
    #         name='stu_modify_message'),
    re_path(r'^stu_home/stu_center/stu_modify_message/(\d+)', views.stu_modify_message, name="stu_modify_message"),
    # 2 学生：公告页 ~~~~ 2
    path('stu_home/stu_notice/', views.stu_notice, name="stu_notice"),
    # 2 学生：进入活动公告 ~~~~ 2
    re_path(r'^stu_home/stu_notice/stu_notice_act/(\d+)', views.stu_notice_act, name="stu_notice_act"),
    # 2 学生：进入系统公告 ~~~~ 2
    re_path(r'^stu_home/stu_notice/mag_notice_sys/(\d+)', views.stu_notice_sys, name="stu_notice_sys"),

    # 组织者 ：主页  ~~~~~
    path('org_home/', views.org_home, name="org_home"),
    # 1 组织者 ：发布活动 ----- (覃智科) ~~~~~
    path('org_home/org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 1 组织者：发布公告 ----- (覃智科) ~~~~~
    path('org_home/org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 2 组织者：公告页  ~~~~ 2
    path('org_home/org_notice/', views.org_notice, name="org_notice"),
    # 系统公告
    re_path(r'^org_home/org_notice/mag_notice_sys/(\d+)', views.org_notice_sys, name="org_notice_sys"),
    # 活动公告
    re_path(r'^org_home/org_notice/mag_notice_act/(\d+)', views.org_notice_sys, name="org_notice_sys"),
    # 2 组织者：查看已发活动 -----（秦浩廷）~~~~~
    path('org_home/org_view_posted_activity/', views.org_view_posted_activity, name="org_view_posted_activity"),
    # 组织者：查看单人活动人员名单
    re_path(r'^org_home/org_view_posted_activity/org_launch_activity_details/org_stu_one_list/(\d+)',
            views.org_stu_one_list, name="org_stu_one_list"),
    # 组织者：已发布活动性详情页
    re_path(r'^org_home/org_view_posted_activity/org_launch_activity_details/(\d+)', views.org_launch_activity_details,
            name="org_launch_activity_details"),
    # 组织者：查看组队活动队伍名单
    re_path(r'^org_home/org_view_posted_activity/org_launch_activity_details/org_stu_team_list/(\d+)',
            views.org_stu_team_list, name="org_stu_team_list"),
    # 组织者：查看具体活动的个具体队伍信息
    re_path(
        r'org_home/org_view_posted_activity/org_launch_activity_details/org_stu_team_list/org_stu_team_list_mul/(\d+)',
        views.org_stu_team_list_mul, name="org_stu_team_list_mul"),
    # 1 2 组织者：修改活动 ~~~~ 1
    path('org_home/org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 2 组织者中心 ~~~~ 2
    path('org_home/org_center/', views.org_center, name="org_center"),
    # 1 2 组织者：修改组织者信息 ~~~~ 1
    path('org_home/org_modify_message/', views.org_modify_message, name="org_modify_message"),
    # 组织者修改活动页
    re_path(r'^org_home/org_view_posted_activity/org_launch_activity_details/org_modify_activity_message/(\d+)',
            views.org_modify_activity_message, name="org_modify_activity_message"),

    # 管理者： 主页
    path('mag_home/', views.mag_home, name='mag_home'),
    # 12管理者：审核
    path('mag_home/mag_examine_act/', views.mag_examine_act, name="mag_examine_act"),
    # 12管理者：审核
    path('mag_home/mag_examine_org/', views.mag_examine_org, name="mag_examine_org"),
    # 12管理者：管理组织者
    path('mag_home/mag_manage/', views.mag_manage, name="mag_manage"),
    # 管理者：发布公告
    path('mag_home/mag_launch_notice/', views.mag_launch_notice, name="mag_launch_notice"),
    # 管理者：公告页面
    path('mag_home/mag_notice/', views.mag_notice, name="mag_notice"),
    # 管理者：进入活动公告的
    re_path(r'^mag_home/mag_notice/mag_notice_act/(\d+)', views.mag_notice_act, name="mag_notice_act"),
    # 管理者：进入系统公告的
    re_path(r'^mag_home/mag_notice/mag_notice_sys/(\d+)', views.mag_notice_sys, name="mag_notice_sys"),
    # 12管理者：审核
    path('mag_home/mag_add_org/', views.mag_add_org, name="mag_add_org"),
    # 很多东西
    re_path(r'^mag_home/mag_examine_act/mag_look_act/(\d+)', views.mag_look_act, name="mag_look_act"),
    re_path(r'^mag_home/mag_examine_org/mag_look_org/(\d+)', views.mag_look_org, name="mag_look_org"),
    re_path(r'^mag_home/mag_manage/mag_look_mag_org/(\d+)', views.mag_look_mag_org, name="mag_look_mag_org"),
    re_path(r'^mag_home/mag_manage/mag_revise/(\d+)', views.mag_revise, name="mag_revise"),
    re_path(r'^mag_home/mag_manage/mag_delete/(\d+)', views.mag_delete, name="mag_delete"),
    path('stu_home/stu_directmessage', views.stu_directmessage, name="stu_directmessage"),
    path('stu_home/stu_bbs', views.stu_bbs, name="stu_bbs"),

]
