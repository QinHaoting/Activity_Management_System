from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
import uuid

from sac_app.check_code import gen_check_code


from io import BytesIO
from django.contrib import auth


def login(request):
    if request.method == 'POST':
        method = request.POST.get('method')    #获取登录信息
        log_id = request.POST.get('username')
        log_password = request.POST.get('password')
        con_code = request.POST.get('idcode')
        check_code = request.session.get('check_code')
        if log_id and log_password and con_code:
            if con_code == check_code:
                if method == 'student':  # 如果选择学生登录
                    try:
                        student = students.objects.get(stu_id=log_id)
                        if student.stu_valid == 1:
                            if student.stu_password == log_password:
                                request.session['user_id'] = student.stu_id
                                request.session['user_type'] = 'student'
                                return RttpResponse('登陆成功')
                            else:
                                return render(request, 'login.html', {'password_error': '密码错误'})
                        else:
                            return render(request, 'login.html', {'valid_error': '账户未激活'})
                    except:
                        return render(request, 'login.html', {'id_error': 'id不存在'})
                elif method == 'organizer':  # 如果选择组织者登录
                    try:
                        organizer = organizers.objects.get(org_id=log_id)
                        if organizer.org_password == log_password:
                            request.session['user_id'] = organizer.org_id
                            request.session['user_type'] = 'organizer'
                            return RttpResponse('登陆成功')
                        else:
                            return render(request, 'login.html', {'password_error': '密码错误'})
                    except:
                        return render(request, 'login.html', {'id_error': 'id不存在'})
                elif method == 'manager':  # 如果选择管理者登录
                    try:
                        manager = managers.objects.get(man_id=log_id)
                        if manager.man_password == log_password:
                            request.session['user_id'] = manager.man_id
                            request.session['user_type'] = 'manager'
                            return RttpResponse('登陆成功')
                        else:
                            return render(request, 'login.html', {'password_error': '密码错误'})
                    except:
                        return render(request, 'login.html', {'id_error': 'id不存在'})
            else:
                return render(request,'login.html',{'code_error':'验证码错误'})
        else:
            return render(request,'login.html',{'fill_in_error':'ID,验证码和密码均不能为空'})
    else:
        return render(request, "login.html")
# Create your views here.

def register(request):
    if request.method == 'POST':
        re_id = request.POST.get('username')    #获取注册信息
        re_Email = requestPOST.get('email')
        re_password = request.POST.get('password')
        con_password = request.POST.get('agpassword')
        con_code = request.POST.get('idcode')
        check_code = request.session.get('check_code')
        if re_id and re_Email and re_password and con_password and con_code:
            if con_code == check_code:
                if re_password == con_password:
                    try:
                        student = students.objects.get(stu_id=re_id)
                        return render(request, 'login.html', {'id_error': '该id已存在'})
                    except:
                        try:
                            student = students.objects.get(stu_Email=re_Email)
                            return render(request, 'login.html', {'Email_error': '该Email已被占用'})
                        except:
                            student = students.objects.create(stu_id=re_id, stu_Email=re_Email,
                                                              stu_password=re_password)
                            token = str(uuid.uuid4()).replace('-', '')  # 生成随机字符串
                            request.session[token] = re_id  # session利用生成的随机字符串存储用户id
                            subject = '学生账号激活'
                            message = '''
                                                欢迎注册使用学生活动中心！亲爱的用户赶快激活使用吧！
                                                <br> <a herf = "http://127.0.0.1:8000/sac_app/active?token={}">点击激活</a>
                                                <br>
                                                                        学生活动中心开发团队
                                                '''.format(token)
                            send_mail(subject=subject, message='', from_email='2912784728@qq.com',
                                      recipient_list=[re_Email, ], html_message=message)  # 给用户邮箱发送用于激活的邮件
                            return RttpResponse('注册成功，请前去激活')
                else:
                    return render(request, 'register.html', {'password_error': '两次输入密码不同'})
            else:
                return render(request,'register.html',{'code_error':'验证码错误'})
        else:
            return render(request,'register.html',{'fill_in_error':'ID，邮箱，密码，确认密码和验证码均不能为空'})
    else:
        return render(request, "register.html")

def stu_active(request):
    token = request.GET.get('token')    #获得token再利用session获得学生id
    re_id = request.session.get(token)
    student = students.objects.get(stu_id = re_id)
    student.stu_valid = 1
    student.save()

def forgetpwd(request):

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
    学生：不可参加队伍
    :param request:
    :return:
    """
    return render(request, 'stu_home/stu_activity_no.html')




def stu_createteam(request):
    """
    学生：学生创建队伍
    :param request:
    :return:
    """
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
    return render(request, 'org_home/org_launch_activity.html')


def org_launch_notice(request):
    """
    组织者：发布公告
    :param request:
    :return:
    """
    return render(request, 'org_home/org_launch_notice.html')


def org_modify_activity(request):
    """
    组织者：修改活动
    :param request:
    :return:
    """
    return render(request, 'org_home/org_modify_activity.html')


def org_view_pasted_activity(request):
    """
    组织者：查看已发布活动
    :param request:
    :return:
    """
    return render(request, 'org_home/org_view_posted_activity.html')


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
