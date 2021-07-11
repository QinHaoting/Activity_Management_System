from django.shortcuts import render
from django.core.mail import send_mail
import uuid

# Create your views here.
token_dict = {}


def stu_active(request):
    token = request.GET.get('token')
    uid = token_dict.get(token)
    student = students.objects.get(org_id = uid)
    student.stu_valid = 1
    student.save()




def stu_register(request):
    if request.method == 'POST':
        re_ID = request.POST.get('stu_id')
        re_Email = request.POST.get('stu_Email')
        re_password = request.POST.get('stu_password')
        if re_ID and re_Email and re_password:
            try:
                student = students.objects.get(stu_id=re_ID)
                return render(request,'',{'':'ID已被注册'})
            except:
                try:
                    student = students.objects.get(stu_Email = re_ID)
                    return render(request,'',{'':'邮箱已被注册'})
                except:
                    students.objects.create(stu_id=re_ID, stu_password=re_password, stu_Email=re_Email)
                    subject = ""
                    message = ""
                    return render(request, '')
        else:
            return render(request,'',{'':'ID，邮箱和密码均不能为空'})
    else:
        return render(request,'')



def org_register(request):
    if request.method == 'POST':
        re_ID = request.POST.get('org_id')
        re_password = request.POST.get('org_password')
        re_orgname = request.POST.get('org_name')
        re_hename = request.POST.get('org_header_name')
        re_hephone = request.POST.get('org_header_phone')
        re_headercollege = request.POST.get('org_header_college')
        if re_ID and re_password and re_orgname and re_hename and re_hephone and re_headercollege:
            try:
                organizer = organizers.objects.get(org_id = re_ID)
                return render(request, '', {'': 'ID已被注册'})
            except:
                try:
                    organizer = organizers.objects.get(org_name=re_orgname)
                    return render(request, '', {'': '组织名已被注册'})
                except:
                    organizer = organizers.objects.create(org_id=re_ID, org_password=re_password, org_name=re_orgname,
                                              org_header_name=re_hename, org_header_phone=re_hephone,
                                              org_header_college=re_headercollege)
                    token = str(uuid.uuid4()).replace('-','')
                    token_dict = {token : organizer.org_id}
                    path = ''.format(token)
                    subject = '组织账号激活'
                    message = '''
                    欢迎注册使用学生活动中心！亲爱的用户赶快激活使用吧！
                    <br> <a herf = '{}'>点击激活</a>
                    <br>
                                            学生活动中心开发团队
                    '''.format(path)
                    send_mail(subject=subject, message=message, from_email='', recipient_list=re_Email,
                              html_message=messgae)
                    return render(request, '')
        else:
            return render(request,'',{'':'ID,密码，组织名，组织者姓名，组织者电话和组织大学均不能为空'})
    else:
        return render(request,'')



def man_login(request):
    if request.method == 'POST':
        log_id = request.POST.get('man_id')
        log_password = request.POST.get('man_password')
        if log_id and log_password:
            try:
                manager = managers.objects.get(man_id=log_id)
                if log_password == manager.man_password:
                    return render(request, '')
                else:
                    return render(request, '',{'':'密码错误'})
            except:
                return render(request,'')
        else:
            return render(request,'',{'':'ID和密码不能为空'})
    else:
        return render(request,'')



def