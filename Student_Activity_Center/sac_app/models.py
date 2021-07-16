from django.db import models

import datetime


# 学生类
class students(models.Model):
    # 学生账号
    stu_id = models.CharField(max_length=64)
    # 学生姓名
    stu_name = models.CharField(max_length=64)
    # 学生登入密码
    stu_password = models.CharField(max_length=128)
    # 学生邮箱
    stu_Email = models.EmailField(max_length=64)
    # 学生号码
    stu_phone = models.CharField(max_length=32, null=True)
    # 学生性别
    stu_gender = models.CharField(max_length=8)
    # 学生学院
    stu_college = models.CharField(max_length=128, null=True)
    # 学生专业
    stu_major = models.CharField(max_length=128, null=True)
    # 学生年级
    stu_grade = models.IntegerField(null=True)
    # 学生个人简介
    stu_introduction = models.TextField(null=True)
    # 学生信息有效标志： 0-删除； 1-有效
    stu_valid = models.IntegerField()


# 活动类
class activities(models.Model):
    # 活动ID
    act_id = models.CharField(max_length=128)
    # 社团名字
    org_name = models.CharField(max_length=128)
    # 活动名称
    act_name = models.CharField(max_length=64, blank=False)
    # 活动开始时间
    act_start_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动结束时间
    act_end_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动负责人名字
    act_organizer_name = models.CharField(max_length=64, null=True)
    # 活动社团表间关系
    act_organizer = models.ForeignKey('organizers', on_delete=models.PROTECT)
    # 活动负责人联系方式
    act_organizer_phone = models.CharField(max_length=32, blank=False)
    # 活动类型 单人0 ，组队1
    act_type = models.IntegerField()
    # 活动已创建队伍数
    act_created_team_number = models.IntegerField(null=True)
    # 活动组队最多人数
    act_max_team_number = models.IntegerField(null=True)
    # 活动组队最少人数
    act_min_team_number = models.IntegerField(null=True)
    # 总的活动组数
    act_team_number = models.IntegerField(null=True)
    # 活动进行状态
    act_state = models.IntegerField(null=True)
    # 活动总人数
    act_total_number = models.IntegerField(null=True)
    # 活动已参加人数
    act_participated_number = models.IntegerField(null=True)
    # 活动报名剩余组数
    act_available_team_number = models.IntegerField(null=True)
    # 活动报名剩余人数
    act_available_number = models.IntegerField(null=True)
    # 活动能否参加状态
    act_flag = models.CharField(max_length=16, blank=False)
    # 活动附件
    act_planning_book = models.FileField(null=True)
    # 活动简介
    act_introduction = models.TextField(blank=False)
    # 多对多表间关系
    # 参加活动人员名单
    act_to_stu_table = models.ManyToManyField(students, through='act_to_stu')
    # 一对多表间关系
    # 参加活动队伍名单
    # act_to_stu_team_table = models.ManyToManyField(teams, through='act_to_team')


# 修改活动信息中间表
class activities_modified(models.Model):
    # 活动ID
    act_id = models.CharField(max_length=128)
    # 活动名称
    act_name = models.CharField(max_length=64, blank=False)
    # 活动开始时间
    act_start_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动结束时间
    act_end_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动负责人名字
    act_organizer_name = models.CharField(max_length=64, null=True)
    # 活动社团表间关系
    # act_organizer = models.ForeignKey('organizers', on_delete=models.PROTECT)
    # 活动负责人联系方式
    act_organizer_phone = models.CharField(max_length=32, blank=False)
    # 活动类型 单人0 ，组队1
    act_type = models.IntegerField()
    # 活动已创建队伍
    act_created_team_number = models.IntegerField()
    # 活动组队最多人数
    act_max_team_number = models.IntegerField()
    # 活动组队最少人数
    act_min_team_number = models.IntegerField()
    # 活动组数
    act_team_number = models.IntegerField()
    # 活动进行状态
    act_state = models.IntegerField()
    # 活动总人数
    act_total_number = models.IntegerField()
    # 活动已参加人数
    act_participated_number = models.IntegerField()
    # 活动报名剩余人数
    act_available_number = models.IntegerField()
    # 活动能否参加状态
    act_flag = models.CharField(max_length=16, blank=False)
    # 活动附件
    act_planning_book = models.FileField(null=True)
    # 活动简介
    act_introduction = models.TextField(blank=False)
    # 有效位
    act_valid = models.IntegerField()
    # 多对多表间关系
    # 参加活动人员名单
    # 一对多表间关系
    # 参加活动队伍名单
    # act_to_stu_team_table = models.ManyToManyField(teams, through='act_to_team')


# 管理员类
class managers(models.Model):
    # 管理员账号
    man_id = models.CharField(max_length=64)
    # 管理员登入密码
    man_password = models.CharField(max_length=64)


# 组织类
class organizers(models.Model):
    # 组织账号
    org_id = models.CharField(max_length=64)
    # 组织姓名
    org_name = models.CharField(max_length=64, blank=False)
    # 组织负责人姓名
    org_header_name = models.CharField(max_length=64, blank=False)
    # 组织账号密码
    org_password = models.CharField(max_length=128)
    # 组织负责人联系方式
    org_header_phone = models.CharField(max_length=32, blank=False)
    # 组织负责人所在学院
    org_header_college = models.CharField(max_length=128, null=True)
    # 组织简介
    org_introduction = models.TextField(blank=False)
    # 组织信息有效标志： 0-删除； 1-有效
    org_valid = models.IntegerField()
    # 承办的活动
    # org_act = models.ForeignKey(activities, on_delete=models.PROTECT)


# 组织修改组织信息中间表单
class organizers_modified(models.Model):
    org_id = models.CharField(max_length=64, null=True)
    org_password = models.CharField(max_length=128)
    org_name = models.CharField(max_length=64)
    org_header_name = models.CharField(max_length=64)
    org_header_phone = models.CharField(max_length=32)
    org_header_college = models.CharField(max_length=64)
    org_introduction = models.TextField()
    org_valid = models.IntegerField()


# 活动已参加学生子表类
class act_to_stu(models.Model):
    # 学生参加的活动对应的ID
    act = models.ForeignKey(activities, on_delete=models.PROTECT)
    # 参加活动的学生对应的ID
    stu = models.ForeignKey(students, on_delete=models.PROTECT)


# class act_to_team(models.Model):
#     # 学生参加的活动对应的ID
#     act_id = models.ForeignKey(activities, on_delete=models.PROTECT)
#     # 参加活动的队伍对应的ID
#     team_id = models.ForeignKey(teams, on_delete=models.PROTECT)

# 参加活动队伍类
class teams(models.Model):
    # 队伍人数
    team_number = models.IntegerField()
    # 队名
    team_name = models.CharField(max_length=64, null=True)
    # 队长名
    team_header_name = models.CharField(max_length=64)
    # 队长联系方式
    team_header_phone = models.CharField(max_length=32)
    # 队成员
    team_members = models.ManyToManyField(students, through="stu_to_team")
    # 队伍参加活动的名称
    team_act = models.ForeignKey(activities, on_delete=models.PROTECT)
    team_introduction = models.CharField(max_length=256, null=True)


# 公告类
class notices(models.Model):
    # 公告标题
    notice_title = models.CharField(max_length=64, blank=False)
    # 创建公告时间
    notices_create_time = models.DateTimeField(default=datetime.datetime.now)
    # 公告内容
    notice_content = models.TextField(blank=False)
    # 公告附件
    notice_appendix = models.FileField(null=True)
    # 公告类型
    notice_tag = models.IntegerField(max_length=1)


# 学生队伍子表类
class stu_to_team(models.Model):
    stu = models.ForeignKey(students, on_delete=models.PROTECT)
    team = models.ForeignKey(teams, on_delete=models.PROTECT)


class bbs_comments(models.Model):
    bbs_id = models.CharField(max_length=64)
    bbs_message = models.TextField()
    bbs_create_time = models.DateTimeField(default=datetime.datetime.now)


class stu_directMessages(models.Model):
    send_id = models.CharField(max_length=64)
    message = models.TextField()
    accept_id = models.CharField(max_length=64)
    message_send_time = models.DateTimeField(default=datetime.datetime.now)
    message_valid = models.IntegerField()


class org_directMessages(models.Model):
    send_id = models.CharField(max_length=64)
    message = models.TextField()
    accept_id = models.CharField(max_length=64)
    message_send_time = models.DateTimeField(default=datetime.datetime.now)
    message_valid = models.IntegerField()