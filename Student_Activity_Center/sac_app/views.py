import enum
import uuid
from functools import wraps
from random import random, randint
from typing import re

import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings

from sac_app.check_code import gen_check_code

from io import BytesIO
from django.contrib import auth

from sac_app.models import activities, organizers, notices, managers, students, teams, act_to_stu, stu_to_team, \
    organizers_modified, activities_modified, bbs_comments, stu_directMessages, org_directMessages


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


def check_login(func):
    """
    检查登录状态
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("user_id"):
            return func(request, *args, **kwargs)
        else:
            request.session['message'] = "当前处于未登录状态，请登录后使用"
            return redirect(reverse('sac_app:login'))

    return inner


@check_login
def logout(request):
    """
    注销：删除所有当前请求相关的session
    """
    request.session.delete()
    return redirect(reverse("sac_app:login"))


def login(request):
    if request.method == 'POST':
        method = request.POST.get('select')  # 获取登录信息
        log_id = request.POST.get('username')
        log_password = request.POST.get('password')
        con_code = request.POST.get('idcode')
        check_code = request.session.get('check_code')
        if con_code.upper() == check_code.upper():
            if method == 'stu':  # 如果选择学生登录
                try:
                    student = students.objects.get(stu_id=log_id)
                    if student.stu_valid == 1:
                        if student.stu_password == log_password:
                            request.session['user_id'] = student.id
                            request.session['user_type'] = 'student'
                            # return render(request, 'stu_home/stu_home.html')
                            return redirect(reverse('sac_app:stu_home'))
                        else:
                            return render(request, 'login.html', {'password_error': '密码错误'})
                    else:
                        return render(request, 'login.html', {'valid_error': '账户未激活'})
                except:
                    return render(request, 'login.html', {'id_error': 'id不存在'})
            elif method == 'org':  # 如果选择组织者登录
                try:
                    organizer = organizers.objects.get(org_id=log_id)
                    if organizer.org_password == log_password:
                        request.session['user_id'] = organizer.id
                        request.session['user_type'] = 'organizer'
                        # return render(request, 'org_home/org_home.html')
                        return redirect(reverse('sac_app:org_home'))
                    else:
                        return render(request, 'login.html', {'password_error': '密码错误'})
                except:
                    return render(request, 'login.html', {'id_error': 'id不存在'})
            elif method == 'mag':  # 如果选择管理者登录
                try:
                    manager = managers.objects.get(man_id=log_id)
                    if manager.man_password == log_password:
                        request.session['user_id'] = manager.man_id
                        request.session['user_type'] = 'manager'
                        # return render(request, 'mag_home/mag_home.html')
                        return redirect(reverse('sac_app:mag_home'))
                    else:
                        return render(request, 'login.html', {'password_error': '密码错误'})
                except:
                    return render(request, 'login.html', {'id_error': 'id不存在'})
        else:
            return render(request, 'login.html', {'code_error': '验证码错误'})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        re_id = request.POST.get('username')  # 获取注册信息
        re_Email = request.POST.get('email')
        re_password = request.POST.get('password')
        con_password = request.POST.get('agpassword')
        con_code = request.POST.get('idcode')
        check_code = request.session.get('check_code')
        if con_code.upper() == check_code.upper():
            if re_password == con_password:
                try:
                    student = students.objects.get(stu_id=re_id)
                    return render(request, 'register.html', {'message': '该id已存在'})
                except:
                    try:
                        student = students.objects.get(stu_Email=re_Email)
                        return render(request, 'register.html', {'message': '该Email已被占用'})
                    except:
                        student = students.objects.create(stu_id=re_id, stu_Email=re_Email,
                                                          stu_password=re_password, stu_valid=0)
                        token = str(uuid.uuid4()).replace('-', '')  # 生成随机字符串
                        request.session[token] = re_id  # session利用生成的随机字符串存储用户id
                        subject = '学生账号激活'
                        message = '''
                                                欢迎注册使用学生活动中心！亲爱的用户赶快激活使用吧！
                                                <br>http://127.0.0.1:8000/sac_app/active?token={}
                                                <br>
                                                                        学生活动中心开发团队
                                                '''.format(token)
                        send_mail(subject=subject, message='', from_email='2912784728@qq.com',
                                  recipient_list=[re_Email], html_message=message)  # 给用户邮箱发送用于激活的邮件
                        # return HttpResponse('注册成功，请前去激活')
                        return redirect(reverse("sac_app:login"))
            else:
                return render(request, 'register.html', {'password_error': '两次输入密码不同'})
        else:
            return render(request, 'register.html', {'code_error': '验证码错误'})
    else:
        return render(request, 'register.html')


def stu_active(request):
    """
    激活函数
    """
    token = request.GET.get('token')  # 获得token再利用session获得学生id
    re_id = request.session.get(token)
    student = students.objects.get(stu_id=re_id)
    student.stu_valid = 1
    student.save()
    return HttpResponse('激活成功，请前去登录')
    # return redirect(reverse("sac_app:login"))


def changepwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        re_password = request.POST.get('password')
        con_password = request.POST.get('agpassword')
        if re_password != con_password:
            return render(request, 'forgetpwd.html', {'password_error': '密码不一致'})
        else:
            token = request.GET.get('token')
            re_id = request.session.get(token)
            stu1 = students.objects.get(stu_id=re_id)
            stu1.stu_password = re_password
            stu1.save()
            return redirect(reverse("sac_app:stu_home"))  # 重定向到首页
    else:
        return render(request, "changepwd.html")


def forgetpwd(request):
    """
    忘记密码页
    """
    if request.method == 'POST':
        re_id = request.POST.get('username')
        re_Email = request.POST.get('email')
        code = request.POST.get('idcode')
        real_code = request.session.get('check_code')
        if students.objects.filter(stu_id=re_id).count == 0:
            return render(request, 'forgetpwd.html', {'no_stu_error': '用户不存在'})
        if code.upper() != real_code.upper():
            return render(request, 'forgetpwd.html', {'check_code_error': '验证码错误'})
        else:
            students.objects.get(stu_id=re_id)
            token = str(uuid.uuid4()).replace('-', '')
            request.session[token] = re_id
            subject = '修改密码'
            # 超链接里面的链接地址根据实际情况修改（修改密码的链接）
            message = '''
                                        ！
                                        <br>http://127.0.0.1:8000/sac_app/changepwd?token={}
                                        <br>
                                                                学生活动中心开发团队
                        '''.format(token)
            send_mail(subject=subject, message='', from_email='2912784728@qq.com',
                      recipient_list=[re_Email], html_message=message)
            return redirect(reverse("sac_app:login"))  # 重定向到登录界面
    else:
        return render(request, "forgetpwd.html")


def check_code(request):
    img, code = gen_check_code()
    obj = BytesIO()
    img.save(obj, format='png')
    request.session['check_code'] = code  # 将验证码保存到session里面
    return HttpResponse(obj.getvalue())


@check_login
def stu_home(request):
    """
    学生：主页
    :param request:
    :return:
    """
    if request.method == "POST":
        de = request.POST.get('delete')
        if stu_directMessages.objects.filter(id=de, message_valid=1).first():
            msg = stu_directMessages.objects.filter(id=de, message_valid=1).first()
            msg.message_valid = 0
            msg.save()
    accept_id = request.session.get('user_id', 1)
    print(accept_id)
    messages = list(stu_directMessages.objects.filter(accept_id=accept_id, message_valid=1))
    count = len(messages)
    return render(request, 'stu_home/stu_home.html', locals())


@check_login
def stu_directmessage(request):
    """
    学生：主页
    :param request:
    :return:
    """
    if request.method == "POST":
        de = request.POST.get('delete')
        if stu_directMessages.objects.filter(id=de, message_valid=1).first():
            msg = stu_directMessages.objects.filter(id=de, message_valid=1).first()
            msg.message_valid = 0
            msg.save()
    accept_id = request.session.get('user_id', 1)
    print(accept_id)
    messages = list(stu_directMessages.objects.filter(accept_id=accept_id, message_valid=1))
    page = request.GET.get('page', 1)
    id1 = request.session.get('user_id')
    comment = stu_directMessages.objects.filter(accept_id=id1, message_valid=1).order_by('message_send_time')
    pgnt = Paginator(comment, 10)
    if int(page) <= pgnt.num_pages:
        comlist = list(pgnt.page(page))
    else:
        page = str(pgnt.num_pages)
        comlist = list(pgnt.page(page))
    if request.method == 'POST':
        accept_id1 = request.POST.get('accept_id')
        if students.objects.filter(stu_id=accept_id1).first() and accept_id != accept_id1:
            message = request.POST.get('message')
            stu_directMessages.objects.create(send_id=id1, message=message, accept_id=accept_id1, message_valid=1)
            page = request.GET.get('page', 1)
            comment = comment = stu_directMessages.objects.filter(accept_id=id1, message_valid=1).order_by(
                'message_send_time')
            pgnt = Paginator(comment, 10)
            if int(page) <= pgnt.num_pages:
                comlist = list(pgnt.page(page))
            else:
                page = str(pgnt.num_pages)
                comlist = list(pgnt.page(page))
            return redirect(reverse('sac_app:stu_home'))
        return render(request, 'stu_home/stu_directmessage.html', locals())
    return render(request, 'stu_home/stu_directmessage.html', locals())


@check_login
def stu_join_activity(request):
    """
    学生：已参加活动   request.session['user_id']
    :param stu_id:
    :param request:models.students.stu_id
    :return:
    """
    if request.method == 'GET':
        user_id = request.session.get("user_id", None)  # 从前端获取user_id
        if user_id:
            pagesize = 10
            stu = students.objects.get(id=user_id)
            acts = stu.activities_set.all()  # 获取对象
            page = request.POST.get('page', 1)
            # 进行分页操作
            pgnt1 = Paginator(acts, 10)  # 分页结果
            page1 = pgnt1.page(page)  # 分页操作后的页
            pagelist = list(page1)  # 处理成序列字典
            return HttpResponse(render(request, 'stu_home/stu_join_activity.html', locals()))
            # 返回对象及分页序列
        else:
            return render(request, 'stu_home/stu_join_activity.html', context={'message': 'No user_id'})
    else:
        return render(request, 'stu_home/stu_join_activity.html', context={'message': 'Do not use GET'})


@check_login
def stu_activity_details(request, id):
    """
    学生：活动详情页
    :return: 根据前端传入的act_id找到特定活动，返回该活动对象
    """
    request.session['curr_act_id'] = id
    stu_id = request.session['user_id']
    stu = students.objects.filter(id=stu_id).first()
    print(stu_id)
    print(stu)
    act = activities.objects.filter(act_id=id).first()
    acts = stu.activities_set.all()
    ok = request.POST.get('ok')
    if act in acts:
        context = {
            "activity": act,
            "control": 0,  # 已参加活动
        }
        return render(request, 'stu_home/stu_activity_details.html', context=context)
    else:
        if act.act_type == 0:
            if ok == "1":  # 单人活动报名
                act_to_stu.objects.create(act_id=id, stu_id=stu.id)
                act.act_available_number = act.act_available_number - 1
                act.save()
                context = {
                    'activity': act,
                    'control': 0  # 单人活动已报名报名
                }
                return render(request, 'stu_home/stu_activity_details.html', context=context)
            else:
                context = {
                    'activity': act,
                    'control': 1,  # 单人活动未报名
                }
                return render(request, 'stu_home/stu_activity_details.html', context=context)
        else:
            context = {
                'activity': act,
                'control': 2  # 多人活动报名
            }
            return render(request, 'stu_home/stu_activity_details.html', context=context)


@check_login
def stu_center(request):
    """'
    个人中心：显示学生的所有可显示信息-2
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        stu = students.objects.filter(id=user_id).first()  # return an object获取对象
        context = {
            'stu': stu
        }
        return render(request, 'stu_home/stu_center.html', context=context)  # 返回对象
    else:
        return render(request, 'stu_home/stu_center.html', context={'message': '消息错误'})


@check_login
def stu_modify_message(request, id):
    """
    学生：修改个人信息
    :param request:
    :return:
    """
    stu1 = students.objects.filter(id=id).first()
    stu2 = students.objects.filter(id=id).first()
    if request.method == "POST":
        id = request.session.get('user_id')
        stu_password = request.POST.get('stu_password')
        print(stu_password)
        stu_Email = request.POST.get('stu_Email')
        print(stu_Email)
        stu_name = request.POST.get('stu_name')
        stu_phone = request.POST.get('stu_phone')
        stu_gender = request.POST.get('stu_gender')
        stu_major = request.POST.get('stu_major')
        stu_college = request.POST.get('stu_college')
        stu_grade = request.POST.get('stu_grade')
        stu_introduction = request.POST.get('stu_introduction')
        stu_valid = request.POST.get('stu_valid')
        stu2.stu_id = id
        stu2.stu_password = stu_password
        stu2.stu_phone = stu_phone
        stu2.stu_gender = stu_gender
        stu2.stu_grade = stu_grade
        stu2.stu_major = stu_major
        stu2.stu_introduction = stu_introduction
        stu2.valid = stu_valid
        print(stu2)
        stu2.save()
        return redirect(reverse('sac_app:stu_center'))
    return render(request, 'stu_home/stu_modify_message.html', {"stu": stu1})


# def stu_modify_message(request, id):
#     """
#     学生：修改个人信息
#     :param request:
#     :return:
#     """
#     print(request.method)
#     if request.method == "GET":
#         stu1 = students.objects.filter(id=id).first()
#         return render(request, 'stu_home/stu_modify_message.html', {"stu": stu1})
#     if request.method == "POST":
#         id = request.session.get('user_id')
#         stu_password = request.POST.get('stu_password')
#         stu_Email = request.POST.get('stu_Email')
#         stu_name = request.POST.get('stu_name')
#         stu_phone = request.POST.get('stu_phone')
#         print(stu_phone)
#         stu_gender = request.POST.get('stu_gender')
#         stu_major = request.POST.get('stu_major')
#         stu_college = request.POST.get('stu_college')
#         stu_grade = request.POST.get('stu_grade')
#         stu_introduction = request.POST.get('stu_introduction')
#         stu_valid = request.POST.get('stu_valid')
#         stu2 = students.objects.filter(id=id).first()
#         stu2.stu_id = request.POST.get('stu_id')
#         stu2.stu_college = stu_college
#         stu2.stu_name = stu_name
#         stu2.stu_Email = stu_Email
#         stu2.stu_password = stu_password
#         stu2.stu_phone = stu_phone
#         stu2.stu_gender = stu_gender
#         stu2.stu_grade = stu_grade
#         stu2.stu_major = stu_major
#         stu2.stu_introduction = stu_introduction
#         stu2.valid = stu_valid
#         stu2.save()
#         return redirect(reverse('sac_app:stu_center'))


@check_login
def stu_activity(request):
    """
    学生：显示活动列表
    根据前端的control信号返回对应的活动列表
    :return: 活动列表
    """
    whole_activities = activities.objects.filter().exclude(act_state=0).exclude(act_state=1).order_by(
        'act_start_time')  # 可显示的活动集
    show_activities = None  # 待显示的活动集 - 筛选后的活动集
    control = 0  # 控制信号，默认显示所有活动
    if request.GET.get('control'):
        control = int(request.GET.get('control'))
    if control == 0:  # 显示所有活动
        show_activities = whole_activities
    elif control == 1:  # 显示可参加活动
        show_activities = whole_activities.filter(act_flag='可参加')
    elif control == 2:  # 显示不可参加活动
        show_activities = whole_activities.filter().exclude(act_flag='可参加')
    # 返回相关活动集
    pagesize = 10
    pgnt1 = Paginator(show_activities, pagesize)
    page = request.POST.get('page', 1)
    page1 = pgnt1.page(page)
    org_list = list(page1)
    if show_activities:  # 待显示的活动不为空
        context = {
            'activities': show_activities,  # <待显示活动对象>列表
            'func_state': 0,  # 访问状态
            'message': '正常访问'  # 消息
        }
        return HttpResponse(render(request, 'stu_home/stu_activity.html', locals()))  # 访问成功
    else:  # 待显示列表为空
        context = {
            'activities': None,  # <待显示活动对象>列表
            "func_state": 1,  # 访问状态
            "message": "待显示的内容为空"
        }
        return HttpResponse(render(request, 'stu_home/stu_activity.html', locals()))


@check_login
def stu_join_activity_details(request, id):
    """
    学生：已参加参加活动
    :param request:
    :return:
    """
    act = activities.objects.filter(act_id=id).first()
    print(act.act_type)
    context = {
        'activity': act
    }
    return render(request, 'stu_home/stu_activity_details.html', context=context)


@check_login
def stu_create_team(request):
    if request.method == "GET":
        return render(request, 'stu_home/stu_create_team.html')
    else:
        stu_id = request.session.get('user_id')
        stu = students.objects.get(stu_id=stu_id)
        act_id = request.session.get('curr_act_id')
        act = activities.objects.get(act_id=act_id)
        team_number = request.POST.get('team_number')
        team_name = request.POST.get('team_name')
        team_header_phone = request.POST.get('team_header_phone')
        new_team = teams.objects.create(team_number=team_number,
                                        team_name=team_name,
                                        team_header_name=stu.stu_name,
                                        team_header_phone=team_header_phone,
                                        team_act=act)
        act.act_created_team_number = act.act_created_team_number + 1
        act.save()
        # 学生与活动表间关系
        act_to_stu.objects.create(act=act, stu=stu)
        # 学生与队伍表间关系
        stu_to_team.objects.create(team=new_team, stu=stu)
        return redirect(reverse('sac_app:stu_join_activity'))


@check_login
def stu_myteam(request):
    stu_id = request.session.get('user_id')
    stu = students.objects.get(id=stu_id)
    if stu:
        try:
            team = stu.teams_set.all().order_by('id')
            pagesize = 10
            pgnt1 = Paginator(team, pagesize)
            page = request.POST.get('page', 1)
            page1 = pgnt1.page(page)
            page = list(page1)
            return HttpResponse(render(request, 'stu_home/stu_myteam.html', {'page': page, 'msg': "ok"}))
        except EmptyPage:
            return HttpResponse(render(request, 'stu_home/stu_myteam.html', {'page': [], 'msg': '队伍为空'}))


@check_login
def stu_view_myteam(request, id):
    team = teams.objects.filter(id=id).first()
    context = {
        'team': team,
        'control': 1,
    }
    return render(request, 'stu_home/stu_view_myteam.html', context=context)


# 查看参加活动的队伍
@check_login
def act_join_other_team(request, id):
    act_id = id
    act = activities.objects.filter(act_id=act_id).first()
    if act:
        try:
            team = list(act.teams_set.all())
            pgnt = Paginator(team, 10)
            pagenum = request.POST.get('page', 1)
            ok = request.POST.get('ok')
            pages = list(pgnt.page(pagenum))
            return render(request, 'stu_home/stu_join_other_team.html', {'page': pages, 'msg': "ok"})
        except EmptyPage:
            return HttpResponse(render(request, 'stu_home/stu_join_other_team.html', {'page': [], 'msg': '队伍为空'}))
    return HttpResponse(render(request, 'stu_home/stu_join_other_team.html', {'msg': '活动不存在'}))


@check_login
def stu_view_other_team(request, id):
    team = teams.objects.filter(id=id).first()
    context = {
        'team': team,
        'control': 1,
    }
    return render(request, 'stu_home/stu_view_other_team.html', context=context)


@check_login
def stu_notice(request):
    """
    学生：公告界面
    :param request:
    :return:
    """
    try:
        pagesize = 10
        qs1 = notices.objects.filter(notice_tag=1).values().order_by('id')  # 'notice_title')
        qs0 = notices.objects.filter(notice_tag=0).values().order_by('id')  # 'notice_title')
        pgnt1 = Paginator(qs1, pagesize)
        pgnt0 = Paginator(qs0, pagesize)
        page = request.POST.get('page', 1)
        page0 = pgnt0.page(page)
        page1 = pgnt1.page(page)
        notice_sys = list(page0)
        notice_act = list(page1)
        print(notice_act)
        return HttpResponse(render(request, 'stu_home/stu_notice.html', locals()))

    except EmptyPage:
        return HttpResponse(render(request, 'stu_home/stu_notice.html', {'notice_act': [], 'notice_sys': []}))


@check_login
def stu_notice_act(request, id):
    """
    学生：公告界面
    :param request:
    :return:
    """
    act = notices.objects.filter(id=id).first()

    return render(request, 'stu_home/stu_notice_act.html', locals())


@check_login
def stu_notice_sys(request, id):
    """
    学生：公告界面
    :param request:
    :return:
    """
    sys = notices.objects.filter(id=id).first()
    return render(request, 'stu_home/stu_notice_sys.html', locals())


@check_login
def org_home(request):
    """
    组织者：主页
    :param request:
    :return:
    """
    return render(request, 'org_home/org_home.html')


@check_login
def org_home(request):
    """
    组织者：主页
    :param request:
    :return:
    """
    if request.method == "POST":
        de = request.POST.get('delete')
        if org_directMessages.objects.filter(id=de, message_valid=1).first():
            msg = org_directMessages.objects.filter(id=de, message_valid=1).first()
            msg.message_valid = 0
            msg.save()
    accept_id = request.session.get('user_id', 1)
    print(accept_id)
    messages = list(org_directMessages.objects.filter(accept_id=accept_id, message_valid=1))

    return render(request, 'org_home/org_home.html', locals())


@check_login
def org_center(request):
    """
    组织者中心：组织者的所有信息（除了id）
    """
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        org = organizers.objects.filter(id=user_id).first()  # return an object获取对象
        context = {
            'org': org
        }
        return render(request, 'org_home/org_center.html', context=context)  # 返回对象
    else:
        return render(request, 'org_home/org_center.html', context={'message': '消息错误'})


@check_login
def org_modify_message(request):
    """
    组织者修改页面：修改组织者信息
    """
    id = request.session.get('user_id')
    org = organizers.objects.filter(id=id).first()
    organizer = organizers.objects.filter(id=id).first()
    if request.method == 'POST':
        organizers_modified.objects.create(
            org_id=id,
            org_password=request.POST.get('password'),
            org_name=request.POST.get('name'),
            org_header_name=request.POST.get('header_name'),
            org_header_phone=request.POST.get('header_phone'),
            org_introduction=request.POST.get('introduction'),
            org_header_college=request.POST.get('header_college'),
            org_valid=1
        )
        return redirect(reverse('sac_app:org_center'))
    return render(request, 'org_home/org_modify_message.html', locals())


@check_login
def org_launch_activity(request):  # 需要修改
    """
    组织者：发布活动，可以不用判断时间重复
    :param request:
    :return:
    """
    id = request.session.get('user_id')
    org = organizers.objects.filter(org_id=id).first()
    if request.method == 'GET':
        return render(request, 'org_home/org_launch_activity.html', {"org": org})
    elif request.method == 'POST':
        # 1.测试开始时间不能晚于结束时间
        # 2.开始时间必须晚于当前时间
        act_start_time = request.POST.get('act_start_time')
        act_start_time = datetime.datetime.strptime(act_start_time, '%Y-%m-%dT%H:%M')  # 字符串转为date.time类型
        act_end_time = request.POST.get('act_end_time')
        act_end_time = datetime.datetime.strptime(act_end_time, '%Y-%m-%dT%H:%M')
        ac = activities.objects.create(
            org_name=request.POST.get("org_name"),
            act_name=request.POST.get('act_name'),
            act_start_time=act_start_time,
            act_end_time=act_end_time,
            act_organizer_name=request.POST.get('act_organizer_name'),
            act_organizer=request.POST.get('act_organizer'),
            act_organizer_phone=request.POST.get('act_organizer_phone'),
            act_max_team_number=request.POST.get('act_max_team_number'),
            act_created_team_number=0,
            act_min_team_number=request.POST.get('act_min_team_number'),
            act_team_number=request.POST.get('act_team_number'),
            act_state=0,  # 0：审核中	1：未发布（不通过）2：报名阶段（通过）	3：进行中	4：已结束
            act_available_team_number=request.POST.get('act_team_number'),
            act_total_number=request.POST.get('act_total_number'),
            act_participated_number=0,
            act_available_number=request.POST.get('act_total_number'),
            act_flag="不可参加",
            act_planning_book=request.POST.get('act_planning_book'),
            act_introduction=request.POST.get('act_introduction'),
            act_type=request.POST.get('act_type'),
            act_organizer_id=id,
        )
        ac.act_id = ac.id
        ac.save()
        return redirect(reverse('sac_app:org_view_posted_activity'))


@check_login
def org_launch_notice(request):
    """
    组织者：发布公告
    :param request:
    :return:
    """
    if request.method != 'POST':
        return render(request, 'org_home/org_launch_notice.html')
    if request.method == 'POST':
        notice_title = request.POST.get('notice_title')
        notice_create_time = request.POST.get('notice_create_time')
        notice_content = request.POST.get('notice_content')
        notice_appendix = request.POST.get('notice_appendix')
        if not (notice_title and notice_create_time and notice_content
                and notice_appendix):
            return render(request, 'org_home/org_launch_notice.html', {'empty_notice_content': '公告所有部分均不能为空'})
        notices.objects.create(
            notice_title=notice_title,
            notice_create_time=notice_create_time,
            notice_content=notice_content,
            notice_appendix=notice_appendix
        )
        return render(request, 'notice/notice.html')


@check_login
def org_modify_activity(request):
    """
    组织者：修改活动
    :param request:
    :return:
    """
    return render(request, 'org_home/org_modify_activity.html')


@check_login
def org_view_posted_activity(request):
    """
    组织者：查看已发布活动
    :return: 组织者已发布活动的列表
    """
    # if request.method == 'POST':  # 正常访问跳转
    if request.session.get("user_type") == 'organizer':  # 组织者登录
        # 获取<组织者>
        org_id = request.session.get("user_id")
        organizer = organizers.objects.get(id=org_id)

        # 根据<组织者>找到其所有活动
        whole_activities = organizer.activities_set.all()

        if whole_activities:  # 组织者有<活动>
            context = {
                'activities': whole_activities,  # 返回活动集
                "func_state": 0,  # 访问状态
                "message": "正常访问"  # 待返回的信息
            }
            return render(request, 'org_home/org_view_posted_activity.html', context=context)
        else:  # 组织者未组织过活动，即无数据显示
            context = {
                'activities': None,  # 返回活动集
                "func_state": 1,  # 访问状态
                "message": "待显示的内容为空"  # 待返回的信息
            }
            return render(request, 'org_home/org_view_posted_activity.html', context=context)
    else:  # 非组织者访问，即参加者或管理员访问，不能显示纤细
        context = {
            'activities': None,  # 返回活动集
            "func_state": 2,  # 访问状态
            "message": "非组织者身份访问，无权限"  # 待返回的信息
        }
        return render(request, 'login.html', context=context)


@check_login
def org_launch_activity_details(request, id):
    """
    组织者：活动详情页
    """
    act = activities.objects.filter(act_id=id).first()
    context = {
        'activity': act
    }
    return render(request, 'org_home/org_launch_activity_details.html', context=context)


@check_login
def org_modify_activity_message(request, id):
    org_id = request.session.get('user_id')
    org = organizers.objects.get(id=org_id)
    act = activities.objects.get(id=id)
    if request.method == 'POST':
        act_start_time = request.POST.get('act_start_time')
        act_start_time = datetime.datetime.strptime(act_start_time, '%Y-%m-%dT%H:%M')  # 字符串转为date.time类型
        act_end_time = request.POST.get('act_end_time')
        act_end_time = datetime.datetime.strptime(act_end_time, '%Y-%m-%dT%H:%M')
        activities_modified.objects.create(
            act_id=id,
            act_name=request.POST.get('act_name'),
            act_start_time=act_start_time,
            act_end_time=act_end_time,
            act_organizer_name=request.POST.get('act_organizer_name'),
            act_organizer_phone=request.POST.get('act_organizer_phone'),
            act_max_team_number=request.POST.get('act_max_team_number'),
            act_team_number=request.POST.get('act_team_number'),
            act_state=0,
            act_total_number=request.POST.get('act_total_number'),
            act_participated_number=act.act_participated_number,
            act_available_number=act.act_available_number,
            act_flag=act.act_flag,
            act_min_team_number=act.act_min_team_number,
            act_created_team_number=act.act_created_team_number,
            act_planning_book=request.POST.get('act_planning_book'),
            act_introduction=request.POST.get('act_introduction'),
            act_type=request.POST.get('act_type'),
            act_valid=1
        )
        act.act_state = 0
        act.save()
        return redirect(reverse('sac_app:org_launch_activity'))
    return render(request, 'org_home/org_modify_activity_message.html', {"act": act, "org": org})


@check_login
def org_stu_one_list(request, id):
    """
    组织者：单人活动人员表单
    """
    act = activities.objects.get(id=id)
    try:
        temp = list(act_to_stu.objects.filter(act=act).values('stu_id'))
        stu = []
        for i in range(len(temp)):
            stu.append(students.objects.get(id=temp[i]['stu_id']))
        pgnt = Paginator(stu, 10)
        pagenum = request.POST.get('page', 1)
        page = list(pgnt.page(pagenum))
        return HttpResponse(render(request, 'org_home/org_stu_one_list.html', {'page': page, 'msg': "ok"}))
    except EmptyPage:
        return HttpResponse(render(request, 'org_home/org_stu_one_list.html', {'page': [], 'msg': '学生为空'}))


@check_login
def org_stu_team_list(request, id):
    """
    组织者：组队活动队伍表单
    """
    act = activities.objects.get(id=id)
    try:
        team = list(act.teams_set.all())
        pgnt = Paginator(team, 10)
        pagenum = request.POST.get('page', 1)
        page = list(pgnt.page(pagenum))
        return HttpResponse(render(request, 'org_home/org_stu_team_list.html', {'page': page, 'msg': "ok"}))
    except EmptyPage:
        return HttpResponse(render(request, 'org_home/org_stu_team_list.html', {'page': [], 'msg': '队伍为空'}))


@check_login
def org_stu_team_list_mul(request, id):
    """
    组织者：查看某个活动某个对的队员信息
    """
    stu_team = teams.objects.get(id=id)
    m = list(stu_to_team.objects.filter(team=stu_team).values('stu_id'))
    member = []
    for i in range(len(m)):
        member.append(students.objects.get(stu_id=m[i]['stu_id']))
    return render(request, 'org_home/org_stu_team_list_mul.html', {"stus": member})


@check_login
def org_notice(request):
    """
    组织者: 公告界面
    :param request:
    :return:
    """
    try:
        pagesize = 10
        qs1 = notices.objects.filter(notice_tag=1).values().order_by('id')  # 'notice_title')
        qs0 = notices.objects.filter(notice_tag=0).values().order_by('id')  # 'notice_title')
        pgnt1 = Paginator(qs1, pagesize)
        pgnt0 = Paginator(qs0, pagesize)
        page = request.POST.get('page', 1)
        page0 = pgnt0.page(page)
        page1 = pgnt1.page(page)
        notice_sys = list(page0)
        notice_act = list(page1)
        print(notice_act)
        return HttpResponse(render(request, 'org_home/org_notice.html', locals()))

    except EmptyPage:
        return HttpResponse(render(request, 'org_home/org_notice.html', {'notice_act': [], 'notice_sys': []}))


@check_login
def org_notice_act(request, id):
    """
    组织者：活动公告界面
    :param request:
    :return:
    """
    return render(request, 'org_home/org_notice_act.html', locals())


@check_login
def org_notice_sys(request, id):
    """
    组织者：系统公告界面
    :param request:
    :return:
    """
    sys = notices.objects.filter(id=id).first()
    return render(request, 'org_home/org_notice_sys.html', locals())


@check_login
def mag_home(request):
    """
    管理者：主页
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_home.html')


@check_login
def mag_examine_act(request):
    """
    管理者：审核
    :param request:
    :return:
    """

    try:
        pagesize = 10
        # if request.method == "POST":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        # page = request.POST.get('page',1)
        qs1 = activities.objects.filter(act_state=0)  # .values().order_by('org_id')#'notice_title')
        qs2 = activities_modified.objects.filter(act_valid=1)
        pgnt1 = Paginator(qs1, pagesize)
        pgnt2 = Paginator(qs2, pagesize)
        page = request.POST.get('page', 1)
        # print(pgnt1.num_pages)
        # print(pgnt1.count)
        page1 = pgnt1.page(page)
        page2 = pgnt2.page(page)
        # print(page)
        # print(page1)
        act1_list = list(page1)
        act2_list = list(page2)
        # print(act_list)
        return HttpResponse(render(request, 'mag_home/mag_examine_act.html', locals()))
    except EmptyPage:
        return HttpResponse(render(request, 'mag_home/mag_examine_act.html', {'org_list': []}))
    except:
        return HttpResponse(render(request, 'mag_home/mag_examine_act.html', {'msg': "未知错误"}))
    # return render(request, 'mag_home/mag_examine_act.html')


@check_login
def mag_add_org(request):
    """
    管理者：增加组织者
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        header_name = request.POST.get('header_name')
        password = request.POST.get('password')
        header_phone = request.POST.get('header_phone')
        header_college = request.POST.get('header_college')
        introduction = request.POST.get('introduction')
        organizers.objects.create(org_id=id, org_name=name, org_header_name=header_name,
                                  org_password=password, org_header_phone=header_phone,
                                  org_header_college=header_college, org_introduction=introduction, org_valid=1)
        return render(request, 'mag_home/mag_add_org.html', {"success": "添加成功"})
    return render(request, 'mag_home/mag_add_org.html')


@check_login
def mag_examine_org(request):
    """
    管理者：审核
    :param request:
    :return:
    """
    try:
        pagesize = 10
        # if request.method == "POST":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        # page = request.POST.get('page',1)
        qs1 = organizers_modified.objects.filter(org_valid=1)  # .values().order_by('org_id')#'notice_title')
        pgnt1 = Paginator(qs1, pagesize)
        page = request.POST.get('page', 1)
        if page > pgnt1.num_pages: page = pgnt1.num_pages
        page1 = pgnt1.page(page)
        org_list = list(page1)
        # print(org_list)
        return HttpResponse(render(request, 'mag_home/mag_examine_org.html', locals()))
    except EmptyPage:
        return HttpResponse(render(request, 'mag_home/mag_examine_org.html', {'org_list': []}))
    except:
        return HttpResponse(render(request, 'mag_home/mag_examine_org.html', {'msg': "未知错误"}))


@check_login
def mag_manage(request):
    """
    管理者：管理组织者
    :param request:
    :return:
    """
    try:
        pagesize = 10

        # if request.method == "POST":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        # page = request.POST.get('page',1)
        qs1 = organizers.objects.filter(org_valid=1)  # .values().order_by('org_id')#'notice_title')
        pgnt1 = Paginator(qs1, pagesize)
        page = request.POST.get('page', 1)
        page1 = pgnt1.page(page)
        org_list = list(page1)
        return HttpResponse(render(request, 'mag_home/mag_manage.html', locals()))
    except EmptyPage:
        return HttpResponse(render(request, 'mag_home/mag_manage.html', {'org_list': []}))
    except:
        return HttpResponse(render(request, 'mag_home/mag_manage.html', {'msg': "未知错误"}))


@check_login
def mag_launch_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        attachment = request.POST.get('attachment')
        notices.objects.create(notice_title=title, notice_content=content, notice_appendix=attachment,
                               notice_tag=0)
        return render(request, 'mag_home/mag_launch_notice.html', {"success": "发布成功"})
    return render(request, 'mag_home/mag_launch_notice.html')


@check_login
def mag_notice(request):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    try:
        pagesize = 10
        qs1 = notices.objects.filter(notice_tag=1).values().order_by('id')  # 'notice_title')
        qs0 = notices.objects.filter(notice_tag=0).values().order_by('id')  # 'notice_title')
        pgnt1 = Paginator(qs1, pagesize)
        pgnt0 = Paginator(qs0, pagesize)
        page = request.POST.get('page', 1)
        page0 = pgnt0.page(page)
        page1 = pgnt1.page(page)
        notice_sys = list(page0)
        notice_act = list(page1)
        print(notice_act)
        return HttpResponse(render(request, 'mag_home/mag_notice.html', locals()))

    except EmptyPage:
        return HttpResponse(render(request, 'mag_home/mag_notice.html', {'notice_act': [], 'notice_sys': []}))


@check_login
def mag_notice_act(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    act = notices.objects.filter(id=id).first()

    return render(request, 'mag_home/mag_notice_act.html', locals())


def mag_notice_sys(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    sys = notices.objects.filter(id=id).first()
    return render(request, 'mag_home/mag_notice_sys.html', locals())


@check_login
def mag_notice_sys(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    sys = notices.objects.filter(id=id).first()
    return render(request, 'mag_home/mag_notice_sys.html', locals())


@check_login
def mag_look_act(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    act = activities.objects.filter(id=id).first()
    act_mid = activities_modified.objects.filter(act_valid=0).first()
    if request.method == 'POST':
        sel = request.POST.get('select')
        if sel == 'yes':
            act.act_name = act_mid.act_name
            act.act_start_time = act_mid.act_start_time
            act.act_end_time = act_mid.act_end_time
            act.act_organizer_name = act_mid.act_organizer_name
            act.act_organizer_phone = act_mid.act_organizer_phone
            act.act_type = act_mid.act_type
            act.act_total_number = act_mid.act_total_number
            act.act_team_number = act_mid.act_team_number
            act.act_min_team_number = act_mid.act_min_team_number
            act.act_max_team_number = act_mid.act_max_team_number
            act.act_planning_book = act_mid.act_planning_book
            act.act_introduction = act_mid.act_introduction
            act.act_state = act_mid.act_state = 2
            act.save()
            act_mid.save()
            return redirect(reverse('sac_app:mag_examine_act'))
        elif sel == 'no':
            act.act_state = act_mid.act_state = 1
            act.save()
            act_mid.save()
            return redirect(reverse('sac_app:mag_examine_act'))
    return render(request, 'mag_home/mag_look_act.html', locals())


@check_login
def mag_look_org(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    org = organizers.objects.filter(id=id).first()
    org_mid = organizers_modified.objects.filter(org_id=id, org_valid=1).first()
    if request.method == 'POST':
        sel = request.POST.get('select')
        if sel == 'yes':
            org.org_id = org_mid.org_id
            org.org_name = org_mid.org_name
            org.org_password = org_mid.org_password
            org.org_header_name = org_mid.org_header_name
            org.org_header_phone = org_mid.org_header_phone
            org.org_header_college = org_mid.org_header_college
            org.org_introduction = org_mid.org_introduction
            org_mid.org_valid = 0
            org.save()
            org_mid.save()
            return redirect(reverse('sac_app:mag_examine_org'))
        elif sel == 'no':
            org_mid.org_valid = 0
            org_mid.save()
            return redirect(reverse('sac_app:mag_examine_org'))
    return render(request, 'mag_home/mag_look_org.html', locals())


@check_login
def mag_look_mag_org(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    org = organizers.objects.filter(org_id=id).first()
    if request.method == 'POST':
        return redirect(reverse('sac_app:mag_manage'))
    return render(request, 'mag_home/mag_look_mag_org.html', locals())


@check_login
def mag_revise(request, id):
    org = organizers.objects.filter(org_id=id).first()
    organizer = organizers.objects.filter(org_id=id).first()
    if request.method == 'POST':
        id1 = request.POST.get('id')
        name = request.POST.get('name')
        password = request.POST.get('password')
        header_name = request.POST.get('header_name')
        header_phone = request.POST.get('header_phone')
        header_college = request.POST.get('header_college')
        introduction = request.POST.get('introduction')
        organizer.org_id = id1
        organizer.org_name = name
        organizer.org_password = password
        organizer.org_header_name = header_name
        organizer.org_header_phone = header_phone
        organizer.org_header_college = header_college
        organizer.org_introduction = introduction
        organizer.save()
        return redirect(reverse('sac_app:mag_manage'))
    return render(request, 'mag_home/mag_revise.html', locals())


@check_login
def mag_delete(request, id):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    org = organizers.objects.filter(org_id=id).first()
    if request.method == 'POST':
        organizer = organizers.objects.filter(org_id=id).first()
        organizer.org_valid = 0
        organizer.save()
        return redirect(reverse('sac_app:mag_manage'))

    return render(request, 'mag_home/mag_delete.html', locals())


@check_login
def stu_bbs(request):
    """
    管理者：私信
    :param request:
    :return:
    """
    # stu = students.objects.filter(stu_id=id).first()
    # for i in range(0,17):
    # bbs_comments.objects.create(bbs_id=randint(10000000,99999999), bbs_message=random())
    # notices.objects.create(notice_id=i+16, notice_title=random(),
    # notice_content=random(),notice_tag = 0)
    page = request.GET.get('page', 1)
    comment = bbs_comments.objects.all().order_by('bbs_create_time')
    pgnt = Paginator(comment, 10)
    comlist = list(pgnt.page(page))
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        com = request.POST.get('com')
        bbs_comments.objects.create(bbs_id=randint(10000000, 99999999), bbs_message=com)
        page = request.GET.get('page', 1)
        comment = bbs_comments.objects.all().order_by('bbs_create_time')
        pgnt = Paginator(comment, 10)
        comlist = list(pgnt.page(page))
        return render(request, 'stu_home/stu_bbs.html', locals())
    return render(request, 'stu_home/stu_bbs.html', locals())
