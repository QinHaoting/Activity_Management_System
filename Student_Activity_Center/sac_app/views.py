import enum
import time
import uuid
from datetime import datetime
from typing import re

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import datetime
from sac_app.check_code import gen_check_code

from io import BytesIO
from django.contrib import auth

from sac_app.models import activities, organizers, notices, managers, students, teams
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from sac_app.models import *


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
        method = request.POST.get('select')  # 获取登录信息
        log_id = request.POST.get('username')
        log_password = request.POST.get('password')
        con_code = request.POST.get('idcode')
        check_code = request.session.get('check_code')
        print(method)
        print(log_id)
        print(log_password)
        print(con_code)
        print(check_code)
        if con_code.upper() == check_code.upper():
            if method == 'tus':  # 如果选择学生登录
                try:
                    student = students.objects.get(stu_id=log_id)
                    if student.stu_valid == 1:
                        if student.stu_password == log_password:
                            request.session['user_id'] = student.stu_id
                            request.session['user_type'] = 'student'
                            return render(request, 'stu_home/stu_home.html')
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
                        request.session['user_id'] = organizer.org_id
                        request.session['user_type'] = 'organizer'
                        return render(request, 'org_home/org_home.html')
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
                        return render(request, 'mag_home/mag_home.html')
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
                        # return render(request, 'login.html', {'message': '注册成功，请激活后登录'})
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
    根据前端的control信号返回对应的活动列表
    :return: 活动列表
    """
    # if request.method == 'POST':  # 正常方式访问
    if request.session.get("user_type") == 'student':  # 学生登录访问
        # 获取待显示活动集
        whole_activities = activities.objects.filter().exclude(act_state=Status.CHECKING)  # 可显示的活动集
        print()
        show_activities = None  # 待显示的活动集 - 筛选后的活动集
        control = request.POST.get('control')  # 控制信号
        if control == Control.whole:  # 显示所有活动
            show_activities = whole_activities
        elif control == Control.can_join:  # 显示可参加活动
            show_activities = whole_activities.filter(act_state=Status.SIGN_UP)
        elif control == Control.cannot_join:  # 显示不可参加活动
            show_activities = whole_activities.filter().exclude(act_state=Status.SIGN_UP)
        # 返回相关活动集
        if show_activities.all().count() != 0:  # 待显示的活动不为空
            context = {
                'activities': show_activities,  # <待显示活动对象>列表
                'func_state': FunctionStatus.NORMAL,  # 访问状态
                'def stu_activity(request):
    """
    学生：显示活动列表
    根据前端的control信号返回对应的活动列表
    :return: 活动列表
    """
    # if request.method == 'POST':  # 正常方式访问
    if request.session.get("user_type") == 'student':  # 学生登录访问
        # 获取待显示活动集
        whole_activities = activities.objects.filter().exclude(act_state=0).exclude(act_state=1)  # 可显示的活动集
        show_activities = None  # 待显示的活动集 - 筛选后的活动集
        control = 0     # 控制信号，默认显示所有活动
        if request.GET.get('control'):
            control = int(request.GET.get('control'))
        if control == 0:  # 显示所有活动
            show_activities = whole_activities
        elif control == 1:  # 显示可参加活动
            show_activities = whole_activities.filter(act_flag='可参加')
        elif control == 2:  # 显示不可参加活动
            show_activities = whole_activities.filter().exclude(act_flag='可参加')
        # 返回相关活动集
        if show_activities:  # 待显示的活动不为空
            context = {
                'activities': show_activities,        # <待显示活动对象>列表
                'func_state': 0,  # 访问状态
                'message': '正常访问'                  # 消息
            }
            return render(request, 'stu_home/stu_activity.html', context=context)  # 访问成功
        else:  # 待显示列表为空
            context = {
                'activities': None,       # <待显示活动对象>列表
                "func_state": 1,  # 访问状态
                "message": "待显示的内容为空"
            }
            print("待显示的内容为空")
            return render(request, 'stu_home/stu_activity.html', context=context)
    else:  # 非学生登录访问（无权限）    前端保证不触发
        context = {
            'activities': None,  # <待显示活动对象>列表
            "func_state": 2,  # 访问状态
            "message": "非学生身份访问，无权限"  # 待返回的信息
        }
        return render(request, 'login.html', context=context)    # 返回到哪？？？
    # else:  # 非正常方式访问（GET）
    #     context = {
    #         'activities': None,                     # <待显示活动对象>列表
    #         "func_state": FunctionStatus.NOT_POST,  # 访问状态
    #         "message": "非正常形式访问，请登录"        # 待返回的信息
    #     }
    #     return render(request, 'login.html', context=context)





def stu_join_activity(request):
    """
    学生：已参加活动   request.session['user_id']
    :param stu_id:
    :param request:models.students.stu_id
    :return:
    """
    if request.method == 'POST':  # 检测是否用Post请求
        user_id = request.session.get("user_id", None)  # 从前端获取user_id
        if user_id:
            # act_id = act_to_stu.objects.filter(user_id=stu_id).values()
            # act = activities.objects.filter(act_id=act_id)

            stu = students.objects.get(stu_id=user_id)
            act = stu.activities_set.all().order_by('act_id')
            # 进行分页操作
            pagesize = request.params['pagesize']
            pagenum = request.params['pagenum']

            pgnt1 = Paginator(act, pagesize)  # 分页结果
            page1 = pgnt1.page(pagenum)  # 分页操作后的页

            pagelist = list(page1)  # 处理成序列字典

            # act_organizer_name = act.act_organizer_name
            # act_name = act.act_name
            # act_state = act.act_state
            # act_flag = act.act_flage
            # value = {
            #     "act_organizer_name": act_organizer_name,
            #     "act_name": act_name,
            #     "act_state": act_state,
            #     "act_flag": act_flag
            # }
            # act=act_to_stu.objects.filter(students__stu_id=user_id).values()
            act_organizer_name = list(act.values('act_organizer_name'))  # 形成序列字典
            act_name = list(act.values('act_name'))
            act_state = list(act.values('act_state'))
            act_flag = list(act.values('act_flag'))

            return JsonResponse({'act_organizer_name': act_organizer_name,  # JsonResponse响应
                                 'act_name': act_name,
                                 'act_state': act_state,
                                 'act_flag': act_flag,
                                 "pagelist": pagelist})
        # return render(request, {"act_list":act_list},'stu_home/stu_join_activity.html')
        else:
            return render(request, 'stu_home/stu_join_activity.html', context={'message': 'No user_id'})
    else:
        return render(request, 'stu_home/stu_join_activity.html', context={'message': 'Do not use GET'})



def stu_center(request):
    """'
    个人中心：显示学生的个人呢信息
    """
    if request.method == 'POST':
        stu = students.objects.values()  # return an object获取对象
        return render(request, 'stu_home/stu_center.html', {'stu': stu})# 返回对象
    else:
        return render(request, 'stu_home/stu_center.html', context={'message': 'Do not use GET'})




def stu_modify_message(request):
    """
    学生：修改个人信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'stu_home/stu_center.html')
    elif request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        stu_password = request.POST.get('stu_password')
        stu_Email = request.POST.get('stu_Email')
        stu_name = request.POST.get('stu_name')
        stu_phone = request.POST.get('stu_phone')
        stu_gender = request.POST.get('stu_gender')
        stu_major = request.POST.get('stu_major')
        stu_college = request.POST.get('stu_college')
        stu_grade = request.POST.get('stu_grade')
        stu_introduction = request.POST.get('stu_introduction')
        stu_valid = request.POST.get('stu_valid')
        if not (stu_id and stu_password and stu_Email and stu_name and stu_phone
                and stu_gender and stu_college and stu_major and stu_grade and stu_introduction and stu_valid):
            return render(request, 'stu_home/stu_center.html')
        try:
            students.objects.filter(stu_id=stu_id).update(
                stu_id,
                stu_password,
                stu_Email,
                stu_name,
                stu_phone,
                stu_gender,
                stu_college,
                stu_major,
                stu_grade,
                stu_introduction,
                stu_valid)
        except:
            return render(request, 'stu_home/stu_center.html', {'modify_error': '修改信息错误'})
        return render(request, 'stu_home/stu_center.html', {'modify_succeed': '修改信息成功'})


def stu_activity_details(request):
    """
    学生：可参加活动
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_activity_yes.html')



def stu_createteam(request):
    """
    学生：学生创建队伍
    :param request:
    :return:
    """
    if request.method == 'POST':
        act_id = request.POST.get('act_id')
        activity = activities.objects.get(act_id=act_id)  # 查找活动
        name = request.POST.get('team_name')
        team_name = act_id + name  # 保证每个活动中队伍不能重名（models里面的team unique属性为True）
        h_name = request.POST.get('team_header_name')
        phone = request.POST.get('team_header_phone')
        num = activity.act_max_team_number
        # if not all([name, h_name, phone]):
        #     return HttpResponseBadRequest('缺少必传参数')
        if activity.act_available_number == 0:
            return render(request, 'stu_home/stu_createteam.html', {'team_name_error': '队伍数已达上限，无法创建'})
        if not name:
            return render(request, 'stu_home/stu_createteam.html', {'team_name_error': '未填写队伍名字'})
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
            activity.save()
        except DatabaseError:
            return render(request, 'stu_home/stu_createteam.html', {'create_team_error': '队伍创建失败'})
        # 创建完队伍重定向到"我的队伍"
        return redirect(reverse('stu_my_team'))

    else:
        return render(request, 'stu_home/stu_createteam.html')


def stu_myteam(request):
    """
    学生：查看我的队伍  （lzf）
    :param request:
    :return:
    """
    stu_id = request.POST.get('stu_id')
    stu = students.objects.get(stu_id=stu_id)
    act_id = request.POST.get('act_id')
    act = activities.objects.get(act_id=act_id)
    stu_team = stu.teams_set.filter(team_act=act)
    if not stu_team:
        return HttpResponse(render(request, '', {'msg': '未参加队伍'}))
    m = list(stu_to_team.objects.filter(team=stu_team).values('stu_id'))
    member = []
    for i in range(len(m)):
        member.append(students.objects.get(stu_id=m[i]['stu_id']))
    return HttpResponse(render(request, '', {'member': member}))
    return render(request, 'stu_home/stu_myteam.html')


def stu_join_team_act(request):
    """
       学生：组队参加活动(查看活动详情后，点击其他队伍，加入其他队伍) （lzf）
       :param request:
       :return:
       """
    stu_id = request.POST.get('stu_id')
    stu = students.objects.get(stu_id=stu_id)
    act_id = request.POST.get('act_id')
    act = activities.objects.get(act_id=act_id)
    team_name = request.POST.get('team_name')
    team_header_phone = request.objects.get('team_header_phone')
    if act.act_created_team_numbers == act.act_max_team_number:
        return HttpResponse(render(request, '', {'msg': '队伍数以满无法创建'}))
    new_team = teams.objects.create(team_number=act.act_team_numbers,
                                    team_name=team_name,
                                    team_header_name=stu.stu_name,
                                    team_header_phone=team_header_phone,
                                    team_act=act)
    return HttpResponse(render(request, '', {'msg': '创建成功', 'team_id': new_team.team_id}))


def stu_otherteam(request):
    """
    学生：查看参加活动的其他队伍 （lzf）
    :param request:
    :return:
    """
    act_id = request.params['act_id']
    act = activities.objects.get(act_id=act_id)
    if act:
        try:
            team = list(act.teams_set.all())
            pgnt = Paginator(team, 10)
            pagenum = request.POST.get('page', 1)
            page = list(pgnt.pag(pagenum))
            return HttpResponse(render(request, '', {'page': page, 'msg': "ok"}))
        except EmptyPage:
            return HttpResponse(render(request, '', {'page': [], 'msg': '队伍为空'}))
        except:
            return HttpResponse(render(request, '', {'msg': '未知错误'}))
    return HttpResponse(render(request, '', {'msg': '活动不存在'}))
    # team = list(act.teams_set.all())
    # return HttpResponse(render(request, '', {'stu': team}))


def stu_notice(request):
    """
    学生：公告界面
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_notice.html')


def stu_notice_act(request):
    """
    学生：公告界面
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_notice_act.html', locals())


def stu_notice_sys(request):
    """
    学生：公告界面
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_notice_sys.html', locals())


def org_home(request):
    """
    组织者：主页
    :param request:
    :return:
    """
    return render(request, 'org_home/org_home.html')



def org_center(request):
    """
    组织者中心：组织者的所有信息（除了id）-2
    """
    if request.method == 'POST':
        manager = managers.objects.values()  # 获取组织者对象
        return render(request, 'org_home/org_center.html', {'manager': manager})  # 返回对象
    else:
        return render(request, 'org_home/org_center.html', context={'message': 'Do not use GET'})


def org_modify_message(request):
    """
    组织者修改页面：修改组织者信息
    """
    if request.method == 'GET':
        org_id = request.GET.get('org_id')  # 需要前端通过GET发送活动ID/或者session等其他方式 反正要获取到活动ID
        organizer1 = organizers.objects.get(org_id=org_id)  # 获取到活动
        # 以下信息需要在该页面显示  前端。。
        context = {
            "org_name": organizer1.values('org_name'),  # 组织名字
            "org_header_name": organizer1.values('org_header_name'),  # 组织负责人姓名
            "org_password": organizer1.values('org_password'),  # 组织账号密码
            "org_header_phone": organizer1.values('org_header_phone'),  # 组织负责人联系方式
            "org_id": organizer1.values('org_id'),  # 组织ID
            "org_header_college": organizer1.values('org_header_college'),  # 组织负责人所在学院
            "org_introduction": organizer1.values('org_introduction'),  # 组织简介
        }
        return render(request, 'org_home/org_modify_message.html', context=context)
    elif request.method == 'POST':
        org_id = request.POST.get('org_id')
        org_name = request.POST.get('org_name')
        org_header_name = request.POST.get('org_header_name')
        org_password = request.POST.get('org_password')
        org_header_phone = request.POST.get('org_header_phone')
        org_header_college = request.POST.get('org_header_college')
        org_introduction = request.POST.get('org_introduction')
        if not (org_id and org_name and org_header_name and org_password,
                org_header_phone and org_header_college and org_introduction):
            return render(request, 'org_home/org_modify_message.html', {'message': '缺少必要信息'})
        try:
            organizer2 = organizers.objects.get(org_id=org_id)
            organizer2.org_name = org_name
            organizer2.org_header_name = org_header_name
            organizer2.org_password = org_password
            organizer2.org_header_phone = org_header_phone
            organizer2.org_header_college = org_header_college
            organizer2.org_introduction = org_introduction
            organizer2.save()
        except:
            return render(request, 'org_home/org_modify_message.html', {'modify_error': '修改信息错误'})
        return render(request, 'org_home/org_modify_message.html', {'modify_succeed': '修改信息成功'})

    return render(request, 'org_home/org_modify_message.html')


def org_launch_activity(request):  # 需要修改
    """
    组织者：发布活动，可以不用判断时间重复
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'org_home/org_launch_activity.html')
    elif request.method == 'POST':
        act_id = request.POST.get('act_id')
        act_name = request.POST.get('act_name')
        # 1.测试开始时间不能晚于结束时间
        # 2.开始时间必须晚于当前时间
        now = datetime.now()  # 获取现在的时间
        act_start_time = request.POST.get('act_start_time')
        act_start_time = datetime.datetime.strptime(act_start_time, '%Y-%m-%d %H:%M')  # 字符串转为date.time类型
        act_end_time = request.POST.get('act_end_time')
        act_end_time = datetime.datetime.strptime(act_end_time, '%Y-%m-%d %H:%M')
        if act_start_time.__le__(now) or act_start_time.__gt__(act_end_time):
            return render(request, 'org_home/org_launch_activity.html', {'time_error': '时间设置错误'})

        act_organizer_name = request.POST.get('act_organizer_name')
        act_organizer_phone = request.POST.get('act_organizer_phone')
        act_max_team_number = request.POST.get('act_max_team_number')
        act_state = 0  # 0：审核中	1：未发布（不通过）2：报名阶段（通过）	3：进行中	4：已结束
        act_total_number = request.POST.get('act_total_number')  # 针对不需要组队的活动而言
        act_participated_number = 0  # 默认已参加人数为0人
        act_available_number = int(act_total_number)  # 默认可参加人数为总人数人
        act_flag = "不可参加"  # 默认不可参加
        act_planning_book = request.POST.get('act_planning_book')
        act_introduction = request.POST.get('act_introduction')

        if not (act_name and act_start_time and act_end_time and act_organizer_name and act_organizer_phone
                and act_max_team_number and act_state and act_total_number and act_participated_number
                and act_available_number and act_flag and act_planning_book and act_introduction):
            return render(request, 'org_home/org_launch_activity.html', {'message': '不能为空'})
        try:
            activities.objects.create(
                act_id=act_id,
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
        notice_id = request.POST.get('notice_id')
        notice_title = request.POST.get('notice_title')
        notice_create_time = request.POST.get('notice_create_time')
        notice_content = request.POST.get('notice_content')
        notice_appendix = request.POST.get('notice_appendix')
        if not (notice_title and notice_create_time and notice_content
                and notice_appendix):
            return render(request, 'org_home/org_launch_notice.html', {'empty_notice_content': '公告所有部分均不能为空'})
        notices.objects.create(
            notice_id=notice_id,
            notice_title=notice_title,
            notice_create_time=notice_create_time,
            notice_content=notice_content,
            notice_appendix=notice_appendix
        )
        return render(request, 'notice/notice.html')


def org_modify_activity(request):
    """
    组织者：修改活动
    :param request:
    :return:
    """
    # 访问更新活动信息的页面
    if request.method == 'GET':
        # 需要得到活动的id
        act_id = request.GET.get('act_id')  # 需要前端通过GET发送活动ID/或者session等其他方式 反正要获取到活动ID
        activity1 = activities.objects.get(act_id=act_id)  # 获取到活动
        # 以下信息需要在该页面显示  前端。。
        context = {
            "act_name": activity1.values('act_name'),  # 活动名称
            "act_start_time": activity1.values('act_start_time'),  # 开始时间
            "act_end_time": activity1.values('act_end_time'),  # 活动状态
            "act_organizer_name": activity1.values('act_organizer_name'),  # 组织者
            "act_organizer_phone": activity1.values('act_organizer_phone'),  # 组织者联系方式
            "act_max_team_number": activity1.values('act_max_team_number'),  # 活动最大队伍数
            "act_total_number": activity1.values('act_total_number'),  # 针对不需要组队的活动而言
            "act_planning_book": activity1.values('act_planning_book'),  # 活动策划书
            "act_introduction": activity1.values('act_introduction'),  # 活动简介
        }
        return render(request, 'org_home/org_launch_activity.html', context=context)
    # 准备提交更新的信息
    elif request.method == 'POST':
        # 需要得到活动的id
        act_id = request.POST.get('act_id')  # 需要前端通过POST发送活动ID/或者session等其他方式 反正要获取到活动ID
        # 以下获取更新的信息
        act_name = request.POST.get('act_name')
        act_start_time = request.POST.get('act_start_time')
        act_end_time = request.POST.get('acct_end_time')
        act_organizer_name = request.POST.get('act_organizer_name')
        act_organizer_phone = request.POST.get('act_organizer_phone')
        act_max_team_number = request.POST.get('act_max_team_number')
        act_state = 0  # 0:审核中 1：报名中 2：活动进行中 3：活动已结束
        act_total_number = request.POST.get('act_total_number')  # 针对不需要组队的活动而言
        # act_participated_number = 0 #默认已参加人数为0人 ？？？？？？？？ 组织者不能设置？？？
        # act_available_number = int(act_total_number) #默认可参加人数为100人 ????????????? 组织者不能设置？？？
        act_flag = "不可参加"  # 默认不可参加
        act_planning_book = request.POST.get('act_planning_book')
        act_introduction = request.POST.get('act_introduction')
        if not (act_name and act_start_time and act_end_time and act_organizer_name and act_organizer_phone
                and act_max_team_number and act_state and act_total_number and act_flag and act_planning_book and act_introduction):
            return render(request, 'org_home/org_modify_activity.html', {'message': '不能为空'})
        try:
            activity2 = activities.objects.get(act_id=act_id)
            activity2.act_name = act_name  # 修改活动名称
            activity2.act_start_time = act_start_time  # 修改开始时间
            activity2.act_end_time = act_end_time  # 修改结束时间
            activity2.act_organizer_name = act_organizer_name  # 修改组织者
            activity2.act_organizer_phone = act_organizer_phone  # 修改组织者联系方式
            activity2.act_max_team_number = act_max_team_number  # 修改最队伍数
            activity2.act_state = act_state  # 修改活动状态
            activity2.act_total_number = act_total_number  # 修改总人数
            # activity2.act_participated_number=act_participated_number,
            activity2.act_available_number = act_total_number - activity2.values('act_participated_number')  # 修改可参加人数
            activity2.act_flag = act_flag  # 参加状态
            activity2.act_planning_book = act_planning_book  # 更新策划书
            activity2.act_introduction = act_introduction  # 更新简介
            activity2.save()  # 保存
        except DatabaseError:
            return render(request, 'org_home/org_modify_activity.html', {'message': '修改活动信息失败'})
        return render(request, 'org_home/org_view_posted_activity.html')



def org_view_posted_activity(request):
    """
    组织者：查看已发布活动
    :return: 组织者已发布活动的列表
    """
    # if request.method == 'POST':  # 正常访问跳转
    if request.session.get("user_type") == 'organizer':  # 组织者登录
        # 获取<组织者>
        org_id = request.session.get("user_id")
        organizer = organizers.objects.filter(org_id=org_id).first()

        # 根据<组织者>找到其所有活动
        whole_activities = organizer.activities_set.all().order_by('-id')

        if whole_activities:  # 组织者有<活动>
            context = {
                'activities': whole_activities,       # 返回活动集
                "func_state": 0,  # 访问状态
                "message": "正常访问"                  # 待返回的信息
            }
            print("正常访问")
            return render(request, 'org_home/org_view_posted_activity.html', context=context)
        else:  # 组织者未组织过活动，即无数据显示
            context = {
                'activities': None,      # 返回活动集
                "func_state": 1,  # 访问状态
                "message": "待显示的内容为空"  # 待返回的信息
            }
            print("待显示的内容为空")
            return render(request, 'org_home/org_view_posted_activity.html', context=context)
    else:  # 非组织者访问，即参加者或管理员访问，不能显示纤细
        context = {
            'activities': None,  # 返回活动集
            "func_state": 2,  # 访问状态
            "message": "非组织者身份访问，无权限"  # 待返回的信息
        }
        print("非组织者身份访问，无权限")
        # return render(request, 'login.html', context=context)
        return redirect(reverse('login'))
    # else:  # 通过get方法访问
    #     context = {
    #         'activities': None,  # 返回活动集
    #         "func_state": FunctionStatus.NOT_POST,  # 访问状态
    #         "message": "非正常形式访问，请登录"  # 待返回的信息
    #     }
    #     return render(request, 'login.html', context=context)


# def org_activity_details(request):
#     """
#     组织者：查看活动详情
#     """
#     return None


def org_notice(request):
    """
    组织者: 公告界面
    :param request:
    :return:
    """
    return render(request, 'org_home/org_notice.html')


def org_notice_act(request):
    """
    组织者：活动公告界面
    :param request:
    :return:
    """
    return render(request, 'org_home/org_notice_act.html', locals())


def org_notice_sys(request):
    """
    组织者：系统公告界面
    :param request:
    :return:
    """
    return render(request, 'org_home/org_notice_sys.html', locals())


"""
    管理员主页
    管理（删除、添加）组织者页面
    管理员膝盖组织者信息页面
"""


def mag_home(request):
    """
    管理者：主页
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_home.html')


def mag_examine_org_home(request):
    """
        管理者：管理（删除修改）组织者主页面
        :param request:
        :return:
        """
    all_organizer = organizers.objects.filter(org_valid=1)  # 选出状态为1的组织者
    return render(request, 'mag_home/mag_manage.html', locals())


def mag_examine_org(request):
    """？？？？？？？？？？
            管理者：检视组织者详情页
            :param request:
            :return:
            """

    org_id = request.GET.get('org_id')
    organizer_modified = organizers_modified.objects(org_id=org_id)  # 一个中间表单，需要创建
    organizer = organizers.objects.get(org_id=org_id)
    mod_password = organizer_modified.org_password
    mod_name = organizer_modified.org_name
    mod_header_name = organizer_modified.org_header_name
    mod_header_phone = organizer_modified.org_header_phone
    mod_header_college = organizer_modified.org_header_college
    mod_introduction = organizer_modified.org_introduction
    org_password = organizer.org_password
    org_name = organizer.org_header_name
    org_header_name = organizer.org_header_name
    org_header_phone = organizer.org_header_phone
    org_header_college = organizer.org_header_college
    org_introduction = organizer.org_introduction
    return render(request, '', locals())  # 未填入地址



def mag_org_past(request):
    """
        管理者：审核通过，更新组织信息，删除中间表
        """
    org_id = request.GET.get('org_id')
    organizer_modified = organizers_modified.objects(org_id=org_id)
    organizer = organizers.objects.filter(org_id=org_id)
    mod_password = organizer_modified.org_password
    mod_name = organizer_modified.org_name
    mod_header_name = organizer_modified.org_header_name
    mod_header_phone = organizer_modified.org_header_phone
    mod_header_college = organizer_modified.org_header_college
    mod_introduction = organizer_modified.org_introduction
    if (organizer.org_password and organizer.org_name and organizer.org_header_name
            and mod_header_phone and mod_header_college and mod_introduction):
        organizers.objects.filter(org_id=org_id).update(
            org_password=organizer_modified.org_password,
            org_header_name=organizer_modified.org_header_name,
            org_name=organizer_modified.org_name,
            org_header_phone=organizer_modified.org_header_phone,
            org_header_college=organizer_modified.org_header_college,
            org_introduction=organizer_modified.org_introduction
            # 活动指标待更新
        )
    organizer_modified.delete()
    return redirect(reverse('sac_app:'))#待填充地址


def mag_org_failed(request):
    """
    管理者：审核未通过，删除提交的中间表
    """
    org_id = request.GET.get('org_id')
    organizer_modified = organizers_modified.objects(org_id=org_id)
    organizer_modified.delete()

    return redirect(reverse('sac_app:'))


# def mag_examine(request):
#     """
#     管理者：审核列表页
#     :param request:
#     :return:
#     """
#     return render(request, 'mag_home/mag_examine.html')


def mag_update_org(request):
    """
        管理者：管理者修改组织者信息
        :param request:
        :return:
        """
    if request.method == 'POST':
        org_id = request.GET.get('org_id')  # 超链接中包含着的组织者id
        organizer = organizers.objects.get(org_id=org_id)
        new_password = request.POST.get('password')
        if new_password != None:  # 进行判断，如果输入不为空则进行更新
            organizer.org_password = new_password
        new_org_name = request.POST.get('org_name')
        if new_org_name != None:
            organizer.org_name = new_org_name
        new_header_name = request.POST.get('header_name')
        if new_header_name != None:
            organizer.org_header_name = new_header_name
        new_header_phone = request.POST.get('header_phone')
        if new_header_phone != None:
            organizer.org_header_phone = new_header_phone
        new_header_college = request.POST.get('header_college')
        if new_header_college != None:
            organizer.org_header_college = new_header_college
        new_introduction = request.POST.get('introduction')
        if new_introduction != None:
            organizer.org_introduction = new_introduction
        organizer.save()  # 保存更新
        return redirect((reverse('sac_app:mag_manage')))
    elif request.method == 'GET':
        return


# 管理者删除组织者
def mag_delete_org(request):
    """
            管理者：删除组织者
            :param request:
            :return:
            """
    org_id = request.GET.get('org_id')  # 从超链接中获取组织者id
    organizer = organizers.objects.get(org_id=org_id)
    organizer.org_valid = 0  # 被删除的组织者valid被设为0
    organizer.save()  # 保存删除
    return redirect(reverse(''))  # 回到管理组织者的界面


def mag_add_org(request):
    """
                管理者：增加组织者
                :param request:
                :return:
                """
    if request.method == 'POST':
        org_id = request.request.get('org_id')
        org_password = request.POST.get('org_password')
        org_name = request.POST.get('org_name')
        org_header_name = request.POST.get('org_header_name')
        org_header_phone = request.POST.get('org_header_phone')
        org_header_college = request.POST.get('org_header_college')
        org_introduction = request.POST.get('org_introduction')
        org_valid = request.POST.get('org_valid')
        organizers.objects.create(org_id=org_id, org_password=org_password, org_name=org_name,
                                  org_header_name=org_header_name, org_header_phone=org_header_phone,
                                  org_header_college=org_header_college, org_introduction=org_introduction,
                                  org_valid=org_valid)
        return redirect(reverse(''))  # 回到管理组织者的页面
    else:
        return render(request, '')



def mag_examine(request):
    """
    管理者：审核列表页-2
    :param request:
    :return:
    """

    # 获取到将要审核的全部活动的信息
    if request.method == 'POST':
        act_list = activities.objects.filter(act_state=0).values()  # 获取对象
        # act = list(act_page)
        # return JsonResponse(request, {"error": 1, "act_page": act}, 'mag_home/mag_examine.html')
        return render(request, 'mag_home/mag_examine.html', {'act_lsit': act_list})  # 返回对象
    else:
        return render(request, 'mag_home/mag_examine.html', {'message': "请用Post登录"})


def mag_act_past(request):
    """
        管理者：#审核活动通过
        """
    act_id = request.GET.get('act_id')
    activity = activities.objects.get(act_id=act_id)
    activity.act_state = 2
    return redirect(reverse('sac_app:mag_examine'))


def mag_act_failed(request):
    """
        管理者：#审核活动未通过
        """
    act_id = request.GET.get('act_id')
    activity = activities.objects.get(act_id=act_id)
    activity.act_state = 1
    return redirect(reverse('sac_app:mag_examine'))


def mag_launch_notice(request):
    """
    管理者：管理发布公告
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = request.POST.get('id')  # 获取用户输入
        title = request.POST.get('title')
        content = request.POST.get('content')
        attachment = request.POST.get('attachment')
        try:  # 公告id判断，id不重复公告方可发出
            notices.objects.get(notice_id=id)
            return render(request, 'mag_home/mag_launch_notice.html', {'messgae': '公告id重复'})
        except:
            notices.objects.create(notice_id=id, title=title, content=content, attachment=attachment)
    return render(request, 'mag_home/mag_launch_notice.html')


def mag_notice(request):
    """
    管理者：公告界面
    :param request:
    :return:
    """

    return render(request, 'mag_home/mag_notice.html', locals())


def mag_notice_act(request):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_notice_act.html', locals())


def mag_notice_sys(request):
    """
    管理者：公告界面
    :param request:
    :return:
    """
    return render(request, 'mag_home/mag_notice_sys.html', locals())
