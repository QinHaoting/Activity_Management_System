# coding=utf-8


from django.conf.urls import url

from Student_Activity_Center.sac_app import views

app_name = "app"
urlpatterns = [
    # 学生：首页
    url(r'^$', views.stu_home, name="stu_home"),
    # 学生:活动大厅
    url(r'^stu_activity', views.stu_activity, name="stu_activity"),
    # 学生：已参加活动页
    url(r'^stu_join_activity/', views.stu_join_activity, name="stu_join_activity"),
    # 学生：可参加活动页
    url(r'^stu_activity_yes/', views.stu_activity_yes, name="stu_activity_yes"),
    # 学习：不可参加活动
    url(r'^stu_activity_no/', views.stu_activity_no, name="stu_activity_no"),
    # 学生：创建队伍
    url(r'^stu_create_team/', views.stu_create_team, name="stu_create_team"),
    # 学生：我的队伍
    url(r'^stu_my_team/', views.stu_my_team, name="stu_my_team"),
    # 学生：其他队伍
    url(r'^stu_other_team/', views.stu_other_team, name="stu_other_team"),
    # 学生：个人中心
    url(r'^stu_center/', views.stu_center, name="stu_center"),
    # 组织者 ：主页
    url(r'^org_home/', views.org_home, name="org_home"),
    # 组织者 ：发布活动
    url(r'^org_launch_activity/', views.org_launch_activity, name="org_launch_activity"),
    # 组织者：发布公告
    url(r'^org_launch_notice/', views.org_launch_notice, name="org_launch_notice"),
    # 组织者：修改活动
    url(r'^org_modify_activity/', views.org_modify_activity, name="org_modify_activity"),
    # 组织者：查看已发活动
    url(r'^org_view_pasted_activity/', views.org_view_pasted_activity, name="org_view_pasted_activity"),
    # 管理者： 主页
    url(r'^mag_home/', views.mag_home, name="mag_home"),
    # 管理者：审核
    url(r'^mag_examine/', views.mag_examine, name="mag_examine"),
    # 管理者：管理组织者
    url(r'^mag_manage/', views.mag_manage, name="mag_manage"),
    # 公告：公告主页
    url(r'^notice/', views.notice, name="notice"),
    # 公告：活动公告
    url(r'^notice_activity/', views.notice_activity, name="notice_activity"),
    # 公告：系统公告
    url(r'^notice_sys/', views.notice_sys, name="notice_sys"),
]