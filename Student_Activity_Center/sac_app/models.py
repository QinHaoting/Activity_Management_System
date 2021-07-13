from django.db import models

import datetime


# 学生类
class students(models.Model):
    stu_id = models.CharField(max_length=128)
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


# 管理员类
class managers(models.Model):
    man_id = models.CharField(max_length=128)
    # 管理员账号
    man_name = models.CharField(max_length=64)
    # 管理员登入密码
    man_password = models.CharField(max_length=64)


# 组织类
class organizers(models.Model):
    org_id = models.CharField(max_length=128)
    # 组织账号
    org = models.CharField(max_length=64)
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


# 活动类
class activities(models.Model):
    act_id = models.CharField(max_length=128)
    # 活动名称
    act_name = models.CharField(max_length=64, blank=False)
    # 活动开始时间
    act_start_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动结束时间
    act_end_time = models.DateField(default=1970 - 1 - 1, blank=False)
    # 活动负责人名字
    act_organizer_name = models.ForeignKey(organizers, blank=False, on_delete=models.PROTECT)
    # 活动负责人联系方式
    act_organizer_phone = models.CharField(max_length=32, blank=False)
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
    # 多对多表间关系
    # 参加活动人员名单
    act_to_stu_table = models.ManyToManyField(students, through='act_to_stu')
    # 一对多表间关系
    # 参加活动队伍名单
    # act_to_stu_team_table = models.ManyToManyField(teams, through='act_to_team')


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


# 公告类
class notices(models.Model):
    notice_id = models.CharField(max_length=128)
    # 公告标题
    notice_title = models.CharField(max_length=64, blank=False)
    # 创建公告时间
    notices_create_time = models.DateTimeField(default=datetime.datetime.now)
    # 公告内容
    notice_content = models.TextField(blank=False)
    # 公告附件
    notice_appendix = models.FileField(null=True)

    notice_tag = models.IntegerField()
# 学生队伍子表类
class stu_to_team(models.Model):
    stu = models.ForeignKey(students, on_delete=models.PROTECT)
    team = models.ForeignKey(teams, on_delete=models.PROTECT)
