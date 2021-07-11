from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings

from sac_app.check_code import gen_check_code


from io import BytesIO
from django.contrib import auth


def login(request):

    return render(request, "login.html")
# Create your views here.

def register(request):

    return render(request, "register.html")

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