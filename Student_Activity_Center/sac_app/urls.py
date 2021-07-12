from django.conf.urls import url
from django.urls import path

from sac_app import views

app_name = "sac_app"

urlpatterns = [
    # 登录
    url(r'^$', views.login, name="login"),
    # 注册
    path('register/', views.register, name="register"),
    # 忘记密码
    path('forgetpwd/', views.forgetpwd, name="forgetpwd"),
    # 学生：首页
    path('stu_home/', views.stu_home, name="stu_home"),
    # 学生:活动大厅
    path('stu_activity/', views.stu_activity, name="stu_activity"),
    # 学生：已参加活动页
    path('stu_join_activity/', views.stu_join_activity, name="stu_join_activity"),
    # 学生：创建队伍
    path('stu_create_team/', views.stu_createteam, name="stu_create_team"),
    # 学生：我的队伍
    path('stu_my_team/', views.stu_myteam, name="stu_my_team"),
    # 学生：其他队伍
    path('stu_other_team/', views.stu_otherteam, name="stu_other_team"),
    # 学生：个人中心
    path('stu_center/', views.stu_center, name="stu_center"),
    # 学生：修改个人信息
    path('stu_modify_message/', views.stu_modify_message, name='stu_modify_message'),
    # 学生：公告页
    path('stu_notice/', views.stu_notice, name="stu_notice"),
    # 组织者 ：主页
    path('org_home/', views.org_home, name="org_home"),
    # 组织者 ：发布活动
    path('org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 组织者：发布公告
    path('org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 组织者：公告页
    path('org_notice/', views.org_notice, name="org_notice"),
    # 组织者：修改活动
    path('org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 组织者：查看已发活动
    path('org_view_pasted_activity/', views.org_view_posted_activity, name="org_view_pasted_activity"),
    # 组织者中心
    path('org_center/', views.org_center, name="org_center"),
    # 组织者：修改组织信息
    path('org_modify_message/', views.org_modify_message, name="org_modify_message"),
    # 管理者： 主页
    path('mag_home/', views.mag_home, name="mag_home"),
    # 管理者：审核
    path('mag_examine/', views.mag_examine, name="mag_examine"),
    # 管理者：管理组织者
    path('mag_manage/', views.mag_manage, name="mag_manage"),
    # 管理者：公告
    path('mag_notice/', views.mag_notice, name="mag_notice"),
    # 管理者：发布系统公告
    path('mag_launch_notice/', views.mag_launch_notice, name="mag_launch_notice"),
]
