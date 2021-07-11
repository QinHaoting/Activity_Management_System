import enum
import uuid
from typing import re

from django.core.mail import send_mail
from django.db import DatabaseError
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings

from sac_app.check_code import gen_check_code


from io import BytesIO
from django.contrib import auth

from sac_app.models import activities, organizers, notices, managers, students, teams


class FunctionStatus(enum.Enum):
    """
    访问状态
    """
    NORMAL = 0  # 正常
    EMPTY = 1  # 待显示的内容为空
    NO_PERMISSION = 2  # 无权限访问
    NOT_POST = 3  # 非POST方式访问


class Control(enum.Enum):
    """
    待显示活动的控制信号
    """
    whole = 0  # 所有活动
    can_join = 1  # 可参加
    cannot_join = 2  # 不可参加


class Status(enum.Enum):
    """
    活动状态常量
    """
    CHECKING = 0  # 审核阶段
    SIGN_UP = 1  # 报名阶段
    ON_GOING = 2  # 进行中
    END = 3  # 已结束


def login(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        log_id = request.POST.get('id')
        log_password = request.POST.get('password')
        if log_id and log_password:
            if type == 'student':
                try:
                    student = students.objects.get(stu_id=log_id)
                    if student.stu_valid == 1:
                        if student.stu_password == log_password:
                            request.session['user_id'] = student.stu_id
                            return redirect()
                        else:
                            return render(request,'login.html',{'password_error':'密码错误'})
                    else:
                        return render(request,'login.html',{'valid_error':'账户未激活'})
                except:
                    return render(request,'login.html',{'id_error':'id不存在'})
            elif type == 'organizer':
                try:
                    organizer = organizers.objects.get(org_id=log_id)
                    if organizer.org_password == log_password:
                        request.session['user_id'] = organizer.org_id
                        return redirect() # ??????????????
                    else:
                        return render(request, 'login.html', {'password_error': '密码错误'})
                except:
                    return render(request, 'login.html', {'id_error': 'id不存在'})
            elif type == 'manager':
                try:
                    manager = managers.objects.get(man_id = log_id)
                    if manager.man_password == log_password:
                        request.session['user_id'] = manager.man_id
                        return redirect() # ??????????????/
                    else:
                        return render(request, 'login.html', {'password_error': '密码错误'})
                except:
                    return render(request, 'login.html', {'id_error': 'id不存在'})
        else:
            return render(request,'',{'fill_in_error':'ID和密码均不能为空'})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        re_id = request.POST.get('stu_id')
        re_Email = request.POST.get('stu_Email')
        re_password = request.POST.get('stu_password')
        if re_id and re_Email and re_password:
            try:
                student = students.objects.get(stu_id=re_id)
                return render(request, 'login.html', {'id_error': '该id已存在'})
            except:
                try:
                    student = students.objects.get(stu_Email=re_Email)
                    return render(request, 'login.html', {'Email_error': '该Email已被占用'})
                except:
                    student = students.objects.create(stu_id=re_id, stu_Email=re_Email, stu_password=re_password)
                    token = str(uuid.uuid4()).replace('-', '')
                    request.session[token] = re_id
                    path = ''.format(token)
                    subject = '学生账号激活'
                    message = '''
                                        欢迎注册使用学生活动中心！亲爱的用户赶快激活使用吧！
                                        <br> <a herf = '{}'>点击激活</a>
                                        <br>
                                                                学生活动中心开发团队
                                        '''.format(path)
                    send_mail(subject=subject, message='', from_email='',
                              recipient_list=[re_Email, ], html_message=message)
                    return render(request, 'login.html')
        else:
            return render(request,'login.html',{'fill_in_error':'ID，邮箱，密码均不能为空'})
    else:
        return render(request, "register.html")


# ！！！！！！！！！！！！！！！！！
def stu_active(request):
    """
    邮箱注册使用
    """
    token = request.GET.get('token')
    re_id = request.session.get(token)
    student = students.objects.get(stu_id=re_id)
    student.stu_valid = 1
    student.save()


def forgetpwd(request):
    if request.method == 'POST':
        re_id = request.POST.get('stu_id')
        re_Email = request.POST.get('stu_Email')
        code = request.POST.get('check_code')
        if not re_id:
            return render(request, 'forgetpwd.html', {'no_id_error': '请填写学号'})
        if not re_Email:
            return render(request, 'forgetpwd.html', {'no_email_error': '请填写邮箱'})
        if not code:
            return render(request, 'forgetpwd.html', {'no_idcode_error': '请填写验证码'})
        if students.objects.filter(stu_id=re_id).count == 0:
            return render(request, 'forgetpwd.html', {'no_stu_error': '用户不存在'})
        else:
            students.objects.get(stu_id=re_id)
            token = str(uuid.uuid4()).replace('-', '')
            request.session[token] = re_id
            path = ''.format(token)     # 根据用户生成修改新密码的超链接
            subject = '学生账号激活'
            message = '''
                                        欢迎注册使用学生活动中心！亲爱的用户赶快激活使用吧！
                                        <br> <a herf = '{}'>点击激活</a>
                                        <br>
                                                                学生活动中心开发团队
                        '''.format(path)
            send_mail(subject=subject, message='', from_email='',
                      recipient_list=[re_Email, ], html_message=message)
            return render(request, 'login.html')
    else:
        return render(request, "forgetpwd.html")


def check_code(request):
    img, code = gen_check_code()
    obj = BytesIO()
    print(obj.getvalue())
    img.save(obj, format='png')
    request.session['check_code'] = code  # 将验证码保存到session里面
    return HttpResponse(obj.getvalue())


def stu_home(request):
    """
    学生：主页
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_home.html')


def stu_activity(request):
    """
    学生：活动大厅
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_activity.html')


def stu_join_activity(request):
    """
    学生：已参加活动
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_join_activity.html')


def stu_center(request):
    """
    学生：个人中心
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_center.html')


def stu_activity_yes(request):
    """
    学生：可参加活动
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_activity_yes.html')


def stu_activity_no(request):
    """
    学生：显示活动列表
    根据前端的control信号返回对应的活动列表
    :return: 活动列表
    """
    if request.method == 'POST':  # 正常方式访问
        if request.session.get("user_type") == 'student':  # 学生登录访问
            # 获取待显示活动集
            whole_activities = activities.objects.filter().exclude(act_state=Status.CHECKING)  # 可显示的活动集
            show_activities = None                                                             # 待显示的活动集 - 筛选后的活动集
            control = request.POST.get('control')   # 控制信号
            if control == Control.whole:            # 显示所有活动
                show_activities = whole_activities
            elif control == Control.can_join:       # 显示可参加活动
                show_activities = whole_activities.filter(act_state=Status.SIGN_UP)
            elif control == Control.cannot_join:    # 显示不可参加活动
                show_activities = whole_activities.filter().exclude(act_state=Status.SIGN_UP)

            if show_activities.all().count() != 0:  # 待显示的活动不为空
                context = {
                    "act_name": show_activities.values('act_name'),                      # 活动名称        - 列表
                    "act_organizer_name": show_activities.values('act_organizer_name'),  # 组织者名称      - 列表
                    "act_state": show_activities.values('act_state'),                    # 活动状态        - 列表
                    "act_flag": whole_activities.values('act_flag'),                     # 活动可否参加状态 - 列表
                    "func_state": FunctionStatus.NORMAL,                                 # 访问状态
                    "message": "正常访问"                                                 # 待返回的信息
                }
                return render(request, 'stu_home/stu_activity_no.html', context=context)  # 访问成功
            else:  # 待显示列表为空
                context = {
                    "act_name": '无',
                    "act_organizer_name": '无',
                    "act_state": '无',
                    "act_flag": '无',
                    "func_state": FunctionStatus.EMPTY,
                    "message": "待显示的内容为空"
                }
                return render(request, 'org_home/org_view_posted_activity.html', context=context)
        else:  # 非学生登录访问（无权限）
            context = {
                "act_name": '无',                                          # 活动名称        - 列表
                "act_organizer_name": '无',                                # 组织者名称      - 列表
                "act_state": '无',                                         # 活动状态        - 列表
                "act_flag": '无',                                          # 活动可否参加状态 - 列表
                "func_state": FunctionStatus.NO_PERMISSION,                # 访问状态
                "message": "非学生身份访问，无权限"                           # 待返回的信息
            }
            return render(request, 'login.html', context=context)
    else:  # 非正常方式访问（GET）
        context = {
            "act_name": '无',                           # 活动名称        - 列表
            "act_organizer_name": '无',                 # 组织者名称      - 列表
            "act_state": '无',                          # 活动状态        - 列表
            "act_flag": '无',                           # 活动可否参加状态 - 列表
            "func_state": FunctionStatus.NOT_POST,      # 访问状态
            "message": "非正常形式访问，请登录"            # 待返回的信息
        }
        return render(request, 'login.html', context=context)


def stu_createteam(request):
    """
    学生：学生创建队伍
    :param request:
    :return:
    """
    if request.method == 'POST':
        act_id = request.POST.get('act_id')
        activity = activities.objects.get(act_id=act_id)    # 查找活动
        name = request.POST.get('team_name')
        team_name = act_id+name     # 保证每个活动中队伍不能重名（models里面的team unique属性为True）
        h_name = request.POST.get('team_header_name')
        phone = request.POST.get('team_header_phone')
        num = activity.act_max_team_number
        # if not all([name, h_name, phone]):
        #     return HttpResponseBadRequest('缺少必传参数')
        if activity.act_available_number == 0:
            return render(request, 'stu_home/stu_createteam.html', {'team_name_error': '队伍数已达上限，无法创建'})
        if not name:
            return render(request,'stu_home/stu_createteam.html', {'team_name_error': '未填写队伍名字'})
        if not h_name:
            return render(request, 'stu_home/stu_createteam.html', {'header_name_error': '未填写队长姓名'})
        if not phone:
            return render(request, 'stu_home/stu_createteam.html', {'header_phone_error': '未填写队长联系方式'})
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return render(request, 'stu_home/stu_createteam.html', {'header_phone_error': '请输入正确的手机号码'})
        try:
            teams.objects.create(team_number=num, team_name=team_name, team_header_name=h_name, team_header_phone=phone)
            # 活动已参加人数(队伍数)+1 可参加-1
            activity.act_participated_number += 1
            activity.act_available_number -= 1
        except DatabaseError:
            return render(request,'stu_home/stu_createteam.html',{'create_team_error':'队伍创建失败'})
        # 创建完队伍重定向到"我的队伍"
        return redirect(reverse('stu_my_team'))

    else:
        return render(request, 'stu_home/stu_createteam.html')


def stu_myteam(request):
    """
    学生：我的队伍
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_myteam.html')


def stu_otherteam(request):
    """
    学生：其他队伍
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_otherteam.html')


def org_home(request):
    """
    组织者：主页
    :param request:
    :return:
    """
    return render(request, 'org_home/org_home.html')


def org_launch_activity(request):
    """
    组织者：发布活动
    :param request:
    :return:
    """
    if request.method != 'GET':
        return render(request, 'org_home/org_launch_activity.html')
    elif request.method == 'POST':
        # act_id = request.POST.get('act_id')
        act_name = request.POST.get('act_name')
        act_start_time = request.POST.get('act_start_time')
        act_end_time = request.POST.get('acct_end_time')
        act_organizer_name = request.POST.get('act_organizer_name')
        act_organizer_phone = request.POST.get('act_organizer_phone')
        act_max_team_number = request.POST.get('act_max_team_number')
        act_state = request.POST.get('act_state')  # 0:审核中 1：报名中 2：活动进行中 3：活动已结束
        act_total_number = request.POST.get('act_total_number')
        act_participated_number = request.POST.get('act_participated_number')
        act_available_number = request.POST.get('act_available_number')
        act_flag = request.POST.get('act_flag')
        act_planning_book = request.POST.get('act_planning_book')
        act_introduction = request.POST.get('act_introduction')
        if not (act_name and act_start_time and act_end_time and act_organizer_name and act_organizer_phone
                and act_max_team_number and act_state and act_total_number and act_participated_number
                and act_available_number and act_flag and act_planning_book and act_introduction):
            return render(request, 'org_home/org_launch_activity.html', {'message': '不能为空'})
        try:
            activities.objects.create(
                # act_id=act_id,
                act_name=act_name,
                act_start_time=act_start_time,
                act_end_time=act_end_time,
                act_organizer_name=act_organizer_name,
                act_organizer_phone=act_organizer_phone,
                act_max_team_number=act_max_team_number,
                act_state=act_state,
                act_total_number=act_total_number,
                act_participated_number=act_participated_number,
                act_available_number=act_available_number,
                act_flag=act_flag,
                act_planning_book=act_planning_book,
                act_introduction=act_introduction,
            )
        except:
            return render(request, 'org_home/org_launch_activity.html', {'message': '创建公告失败'})
        return render(request, 'org_home/org_view_posted_activity.html')


def org_launch_notice(request):
    """
    组织者：发布公告
    :param request:
    :return:
    """
    if request.method != 'POST':
        return render(request, 'org_home/org_launch_notice.html')
    if request.method == 'POST':
        # notice_id = request.POST.get('notice_id')
        notice_title = request.POST.get('notice_title')
        notice_create_time = request.POST.get('notice_create_time')
        notice_content = request.POST.get('notice_content')
        notice_appendix = request.POST.get('notice_appendix')
        if not (notice_title and notice_create_time and notice_content
                and notice_appendix):
            return render(request, 'org_home/org_launch_notice.html', {'empty_notice_content': '公告所有部分均不能为空'})
        notices.objects.create(
            # notice_id = notice_id,
            notice_title = notice_title,
            notice_create_time = notice_create_time,
            notice_content = notice_content,
            notice_appendix = notice_appendix
        )
        return render(request, 'notice/notice.html')



def org_modify_activity(request):
    """
    组织者：修改活动
    :param request:
    :return:
    """
    return render(request, 'org_home/org_modify_activity.html')


def org_view_posted_activity(request):
    """
    组织者：查看已发布活动
    :return: 组织者已发布活动的列表
    """
    if request.method == 'POST':    # 正常访问跳转
        if request.session.get("user_type") == 'organizer':  # 组织者登录
            # 获取<组织者的名称>
            org_id = request.session.get("user_id")
            org_name = organizers.objects.filter(org_id=org_id).get("org_name")

            # 根据<组织者的名称>找到其所有活动
            whole_activities = activities.objects.filter(act_organizer_name=org_name)

            if whole_activities.all().count() != 0:  # 组织者有<活动>
                context = {
                    'act_name': whole_activities.values('act_name'),                                # 活动名称
                    'act_start_time': whole_activities.values('act_start_time'),                    # 活动开始时间
                    'act_end_time': whole_activities.values('act_end_time'),                        # 活动结束时间
                    'act_state': whole_activities.values('act_state '),                             # 活动进行状态
                    'act_total_number': whole_activities.values('act_total_number'),                # 活动总人数
                    'act_participated_number': whole_activities.values('act_participated_number'),  # 活动已参加人数
                    'act_available_number': whole_activities.values('act_available_number'),        # 活动剩余人数
                    "func_state": FunctionStatus.NORMAL,                                            # 访问状态
                    "message": "正常访问"                                                            # 待返回的信息
                }
                return render(request, 'org_home/org_view_posted_activity.html', context=context)
            else:  # 组织者未组织过活动 - （待改）
                context = {
                    "act_name": '无',                     # 活动名称
                    'act_start_time': '无',               # 活动开始时间
                    'act_end_time': '无',                 # 活动结束时间
                    'act_state': '无',                    # 活动进行状态
                    'act_total_number': '无',             # 活动总人数
                    'act_participated_number': '无',      # 活动已参加人数
                    'act_available_number': '无',         # 活动剩余人数
                    "func_state": FunctionStatus.EMPTY,   # 访问状态
                    "message": "待显示的内容为空"           # 待返回的信息
                }
                return render(request, 'org_home/org_view_posted_activity.html', context=context)
        else:  # 参加者或管理员访问
            context = {
                "act_name": '无',                             # 活动名称
                'act_start_time': '无',                       # 活动开始时间
                'act_end_time': '无',                         # 活动结束时间
                'act_state': '无',                            # 活动进行状态
                'act_total_number': '无',                     # 活动总人数
                'act_participated_number': '无',              # 活动已参加人数
                'act_available_number': '无',                 # 活动剩余人数
                "func_state": FunctionStatus.NO_PERMISSION,   # 访问状态
                "message": "非组织者身份访问，无权限"             # 待返回的信息
            }
            return render(request, 'login.html', context=context)
    else:  # 通过get方法访问
        context = {
            "act_name": '无',                         # 活动名称
            'act_start_time': '无',                   # 活动开始时间
            'act_end_time': '无',                     # 活动结束时间
            'act_state': '无',                        # 活动进行状态
            'act_total_number': '无',                 # 活动总人数
            'act_participated_number': '无',          # 活动已参加人数
            'act_available_number': '无',             # 活动剩余人数
            "func_state": FunctionStatus.NOT_POST,    # 访问状态
            "message": "非正常形式访问，请登录"          # 待返回的信息
        }
        return render(request, 'login.html', context=context)


def mag_home(request):
    """
    管理者：主页
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_home.html')


def mag_examine(request):
    """
    管理者：审核
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_examine.html')


def mag_manage(request):
    """
    管理者：管理组织者
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_manage.html')


def notice(request):
    """
    公告:主页
    :param request:
    :return:
    """
    return render(request, 'notice/notice.html')


def notice_activity(request):
    """
    公告：活动发布
    :param request:
    :return:
    """
    return render(request, 'notice/notice_activity.html')


def notice_sys(request):
    """
    公告：系统发布
    :param request:
    :return:
    """
    return render(request, 'notice/notice_sys.html')
