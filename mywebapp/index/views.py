from django import http
from django.db import connection, connections
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import  login,logout
from django.contrib.auth import authenticate
import os
import shutil
import json
import pymysql
import cv2
from django.conf import settings
from index.models import mission_urls, missions, pic_urls,labels
import random
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import oss2




#Create your views here.
def index(request):
    content = [100]
    content.append(20)
    content.append(request.POST.get('video'))
    content2 = 'hello'
    return render(request,"video.html",{'correct':content,'incorrect':content2})
def upload(request):                      # 设置路径
    if request.method == 'POST':# 获取对象
        cursor = connection.cursor()
        obj = request.FILES.get('fafafa')
        if not os.path.exists(os.path.join('D:\\webapp\\mywebapp\\index\\templates', 'static', 'pic',request.user.username)):
            os.mkdir(os.path.join('D:\\webapp\\mywebapp\\index\\templates', 'static', 'pic',request.user.username))
        f = open(os.path.join('D:\\webapp\\mywebapp\\index\\templates', 'static', 'pic', request.user.username,obj.name), 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        os.chdir(os.path.join('D:\\webapp\\mywebapp\\index\\templates', 'static', 'pic',request.user.username))
        dir_path2 = os.getcwd()
        dirs = os.listdir(dir_path2)                    # 获取指定路径下的文件
        for video_name in dirs:                             # 循环读取路径下的文件并筛选输出
            if os.path.splitext(video_name)[0] == os.path.splitext(obj.name)[0]:   # 筛选此文件 
                break

        output_img_path0 = os.path.join('D:\\webapp\\mywebapp\\index\\', 'static','pic',request.user.username)
        output_img_path1 = os.path.join('D:\\webapp\\mywebapp\\index\\', 'static','pic',request.user.username,os.path.splitext(obj.name)[0]+'image')
        if not os.path.exists(output_img_path0):
            os.mkdir(output_img_path0)

        cap = cv2.VideoCapture(video_name)   

        cnt = 1
        
        while(1):
            ret, frame = cap.read()
            # show a frame
            if ret is True:
                cnt=cnt+1
                if cnt % 10 == 1:
        #            cropped = frame[1075:128, 119:1397]  # 裁剪坐标为[y0:y1, x0:x1]
                    cropped = frame[120:750, 260:1660]  # 裁剪坐标为[y0:y1, x0:x1]
                    output_name = "%s%s%s"%(output_img_path1,str(int(cnt/10)),'.jpg')
                    cv2.imwrite(output_name, cropped)
            else:
                break       
        cnt_pic = int(cnt/10)
        cap.release()
        cv2.destroyAllWindows()
        #description = request.POST.get('description')
        #puber = request.user.username
        #state = '0'
        #pic_num = cnt_pic
        #m = missions.objects.create(description = description,puber=puber,state=state,pic_num=pic_num)
        path1 = []
        for i in range(1,cnt_pic+1):
            ps = '/static/pic/'+request.user.username+'/'+os.path.splitext(obj.name)[0]+'image'+str(i)+'.jpg'
            cursor.execute("insert into index_pic_urls(pic_url,puber)values('{0}','{1}')".format(ps,request.user.username))
            path1.append(ps)
        return render(request, 'video.html',{"path1":path1})
    else:
        return render(request,'video.html')


# 用户账号密码，第三部说明的Access
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
# 获取的AccessKey
auth = oss2.Auth('LTAI5tAgwL6qpoFcfcp2m3La', 'K4vMTbm3rAsVqu43jQADrpYdfl0Ntu')
# 这个是需要用特定的地址，不同地域的服务器地址不同，不要弄错了
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
# 你的项目名称，类似于不同的项目上传的文件前缀url不同
# 因为我用的是ajax传到后端方法接受的是b字节文件，需要如下配置。 阿里云oss支持更多的方式，下面有链接可以自己根据自己的需求去写
bucket = oss2.Bucket(auth, endpoint, 'bs-21-fall')  # 项目名称

# 这个是上传文件后阿里云返回的uri需要拼接下面这个url才可以访问，根据自己情况去写这步
base_file_url = 'https://bs-21-fall.oss-cn-hangzhou.aliyuncs.com/'


# 进度条
# 当无法确定待上传的数据长度时，total_bytes的值为None。
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')


def update_fil_file(file,file_name,file_type):
    """
    ！ 上传文件
    :param file: b字节文件
    :return: 若成功返回文件路径，若不成功返回空
    """
    # 生成文件名
    base_fil_name = file_name + file_type
    # 生成外网访问的文件路径
    file_url = base_file_url + base_fil_name
    # 这个是阿里提供的SDK方法 bucket是调用的4.1中配置的变量名
    res = bucket.put_object(base_fil_name, file, progress_callback=percentage)
    # 如果上传状态是200 代表成功 返回文件外网访问路径
    # 下面代码根据自己的需求写
    if res.status == 200:
        return file_url
    else:
        return False


@csrf_exempt
def pub_pic(request):
    if request.method == 'POST':
        # 获取 上传的 图片信息
        img = request.FILES.getlist('img')

        check_box_list = request.POST.getlist('check_box_list')
        # 获取上传图片的名称

        if not os.path.exists(os.path.join(os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username))):
                os.mkdir(os.path.join(os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username)))
        cnt = 0
        # 写入 上传图片的 内容
        f_urls = []
        for imgs in img:
            img_name = imgs.name
            file = imgs.read()
            for c_l in check_box_list:
                if c_l:
                    file_url = update_fil_file(file,os.path.splitext(img_name)[0],os.path.splitext(img_name)[1])
                    f_urls.append(file_url)
            img_path = os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username, img_name)
            with open(img_path, 'ab') as fp:
                for chunk in imgs.chunks():
                    fp.write(chunk)
                cnt += 1
                fp.close()
        cursor = connection.cursor()
        #description = request.POST.get('description')
        puber = request.user.username
        #state = '0'
        #pic_num = cnt
        #m = missions.objects.create(description = description,puber=puber,state=state,pic_num=pic_num)
        path1 = []
        for imgs in img:
            img_name = imgs.name
            ps = '/static/pic/'+puber+'/'+os.path.splitext(img_name)[0]+os.path.splitext(img_name)[1]
            cursor.execute("insert into index_pic_urls(pic_url,puber)values('{0}','{1}')".format(ps,request.user.username))
            path1.append(ps)
        return render(request,"pic.html",{"f":f_urls})
    else:
        return render(request,"pic.html")
def showmissions(request):
    cursor = connection.cursor()
    cursor.execute("select mission_id,state,puber,recieve,pic_num,description from index_missions")
    mission_info = cursor.fetchall()
    list1 = []
    for m in  mission_info:
        s = ''
        if m[1] == '0':
            s = '未完成'
        if m[1] == '2':
            s = '已完成'
        if m[1] == '1':
            s = '审核中'
        list1.append((m[0],s,m[2],m[3],m[4],m[5]))
    return render(request,"show_missions.html",{"mission_info":list1})
def home(request):
    return render(request,"home.html")
def reg(request):
    return render(request,"reg.html")
def register(request):
    if request.method == 'POST':
        valid = request.POST.get('valid')
        if valid == "":
            cursor = connection.cursor()
            name = request.POST.get('username')
            psswd = request.POST.get('password')
            e_mail = request.POST.get('email')
            cursor.execute("select * from auth_user where username='%s'"%(name))
            count = cursor.fetchall()
            if(count == ()):
                cursor.execute("select * from auth_user where email='%s'"%(e_mail))
                count = cursor.fetchall()
                if(count == ()):
                    User.objects.create_user(username=name,password=psswd,email= e_mail)
                    return render(request,"home.html")
                else:
                    return HttpResponse("重复的邮箱")
            else:
                return HttpResponse("重复用户名")
        else:
            return render(request,"reg.html")
    else:
        return render(request,"reg.html")
def sign_in(request):
    return render(request,"signin.html")
def signin(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(username=name, password=password)
        if not user_obj:
            return HttpResponse("错误的用户名或密码")
        else:
            login(request,user_obj)
            return render(request,"home.html",{"path1":request.user.username})
def log_out(request):
    logout(request)
    return render(request,"home.html")
def act(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        xMin = request.POST.get('xMin')
        yMin = request.POST.get('yMin')
        height = request.POST.get('height')
        width = request.POST.get('width')    
        label = request.POST.get('label')
        pic_num = request.POST.get('pic_num')
        mission = request.POST.get('mid')
        pic_url = request.POST.get('pic_url')
        cursor.execute("select pic_num from index_labels where mission = {1} and pic_num = {0}".format(mission,pic_num))
        res = cursor.fetchall()
        if not res:
            labels.objects.create(xMin = xMin,yMin = yMin,height = height, width = width ,label = label,pic_num = pic_num,mission = mission,pic_url = pic_url)
            cursor.execute("select pic_num from index_missions where mission_id = {0}".format(mission))
            res = cursor.fetchall()
            if res[0][0] == int(pic_num):
                cursor.execute("update index_missions set state = 1 where mission_id = {0}".format(mission))
                return
            else:
                return
        else:
            label = '\'' + label + '\''
            cursor.execute("update index_labels set xMin = {0}, yMin = {1}, height = {2}, width = {3}, label = {4} where pic_num = {5} and mission = {6}".format(xMin,yMin,height,width,label,pic_num,mission)) 
            if  res[0][0] == int(pic_num):
                cursor.execute("update index_missions set state = 1 where mission_id = {0}".format(mission))
                return
            else:
                return
    return HttpResponse('请通过正确渠道访问')
def get_mission(request):
    if request.method == 'GET':
        if request.user.username == '':
            return HttpResponse('请先登录')
        mid = request.GET.get('mid')
        cursor = connection.cursor()
        cursor.execute('select recieve,state from index_missions where mission_id = {0}'.format(mid))
        r_now = cursor.fetchall()
        if r_now[0][0] != '' and r_now[0][0] != request.user.username:
            return HttpResponse('当前任务已经被其他人领取')
        if r_now[0][0] == request.user.username :
            return HttpResponse('当前任务已经被您领取')
        if r_now[0][1] == '2' or r_now[0][1] == '1':
            return HttpResponse("任务状态异常，不能领取")
        r = '\''+request.user.username+'\''
        cursor.execute('update index_missions set recieve = {0} where mission_id = {1}'.format(r,mid))
        return HttpResponse('任务'+mid+'领取成功')
    else:
        return HttpResponse('请通过正确渠道访问')
def go_mark(request):
    if request.method == 'GET':
        if request.user.username == '':
            return HttpResponse('请先登录')
        
        mid = request.GET.get('mid')
        cursor = connection.cursor()
        cursor.execute('select recieve from index_missions where mission_id = {0}'.format(mid))
        r_now = cursor.fetchall()
        if r_now[0][0] != request.user.username:
            return HttpResponse('当前任务已经被其他人领取')
        cursor.execute('select pic_url from index_mission_urls where mission = {0}'.format(mid))
        urls = cursor.fetchall()
        path1 = []
        for url in urls:
            path1.append(url[0])
        return render(request,'mark.html',{"path1":path1,"mid":mid})
    else:
        return HttpResponse('请通过正确渠道访问')
def pub_mission(request):
    cursor = connection.cursor()
    cursor.execute("select id,pic_url from index_pic_urls where puber = '%s'"%(request.user.username))
    urls = cursor.fetchall()
    pic_path = []
    for url in urls:
        pic_path.append((url[0],url[1]))
    return render(request,'release_mission.html',{"a":pic_path})
def do_pub_mission(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('check_box_list')
        if check_box_list:
            cnt = 0
            description = request.POST.get('description')
            if  not description:
                return HttpResponse("备注不能为空")
            puber = request.user.username
            state = '0'
            for img_url in check_box_list:
                cnt += 1
            pic_num = cnt
            m = missions.objects.create(description = description,puber=puber,state=state,pic_num=pic_num)
            for img_url in check_box_list:
                mission_urls.objects.create(pic_url = img_url,mission = m.mission_id)
            return HttpResponse("任务发布成功")
        else:
            return HttpResponse("请选择图片")
    else:
        return HttpResponse("请通过正常渠道访问")
def out_put(request):
    if request.method == 'GET':
        mission_id = request.GET.get('mission_id')
        cursor = connection.cursor()
        cursor.execute('select state,puber from index_missions where mission_id = {0}'.format(mission_id))
        count_down = cursor.fetchall()
        if count_down[0][0] == '1':
            if count_down[0][1] != request.user.username:
                return HttpResponse("此任务正在审核中，请耐心等待")
            else:
                cursor.execute('select count(*) from index_labels where mission = {0}'.format(mission_id))
                count_down = cursor.fetchall()
                ret1 = count_down[0][0]
                cursor.execute('select pic_num from index_missions where mission_id = {0}'.format(mission_id))
                count_down = cursor.fetchall()
                ret2 = count_down[0][0]
                cursor.execute('select * from index_labels where mission = {0}'.format(mission_id))
                labels = cursor.fetchall()
                cursor.execute('select recieve from index_missions where mission_id = {0}'.format(mission_id))
                rec = cursor.fetchall()
                recieve = rec[0][0]
                label_return = []
                judge = True
                for label in labels:
                    label_return.append((label[0],label[1],label[2],label[3],label[4],label[5],label[6],label[7],label[8]))
                return render(request,"output.html",{"ret1":ret1,"ret2":ret2,"label_return":label_return,"judge":judge,"recieve":recieve,"output":output})
        cursor.execute('select count(*) from index_labels where mission = {0}'.format(mission_id))
        count_down = cursor.fetchall()
        cursor.execute('select recieve from index_missions where mission_id = {0}'.format(mission_id))
        rec = cursor.fetchall()
        recieve = rec[0][0]
        if count_down[0][0] > 0:
            cursor.execute('select * from index_labels where mission = {0}'.format(mission_id))
            labels = cursor.fetchall()
            label_return = []
            output_xml = []
            output_xml.append("<annotate><mission>"+str(labels[0][7])+"</mission>")
            output_json = []
            output_json.append({"mission_id":mission_id,"reciever":recieve})
            for label in labels:
                pic_num = label[6]
                label_return.append((label[0],label[1],label[2],label[3],label[4],label[5],label[6],label[7],label[8]))
                x1 = label[1]
                x2 = label[1]+label[4]
                x3 = label[1]
                x4 = label[1]+label[4]
                y1 = label[2]
                y2 = label[2]+label[3]
                y3 = label[2]
                y4 = label[2]+label[3]
                output_xml.append("<url>"+str(label[8])+"</url>"+"<content><x1>"+str(x1)+"</x1>"+"<y1>"+str(y1)+"</y1>"+"<x2>"+str(x2)+"</x2>"+"<y2>"+str(y2)+"</y2>"+"<x3>"+str(x3)+"</x3>"+"<y3>"+str(y3)+"</y3>"+"<x4>"+str(x4)+"</x4>"+"<y4>"+str(y4)+"</y4></content>"+"<rectMask><xMin>"+str(label[1])+"</xMin><yMin>"+str(label[2])+"</yMin><width>"+str(label[4])+"</width><height>"+str(label[3])+"</height></rectMask>"+"<labels></labelName>"+str(label[5])+"<labelColor>red</labelColor><pic_num>"+str(label[6])+"<pic_num></labels><contentType>rect<contentType>")
                content = []
                content.append({"x":x1,"y":y1})
                content.append({"x":x2,"y":y2})
                content.append({"x":x3,"y":y3})
                content.append({"x":x4,"y":y4})
                output_json.append({"url":label[8],"content":content,"rectMask": {
                        "xMin": label[1],
                        "yMin": label[2],
                        "width": label[4],
                        "height": label[3]
                    },"labels": {
                        "labelName": label[5],
                        "labelColor": "red",
                        "labelColorRGB": "255,0,0",
                        "pic_num": label[6]
                    },"contentType": "rect"})
            return render(request,'output.html',{"output_xml":json.dumps(output_xml),"mid":mission_id,"output_json":json.dumps(output_json,separators=(',',':')),"label_return":label_return,"recieve":recieve,"pic_num":pic_num})
        else:
            return HttpResponse("此任务还未完成标注")
    else:
        return HttpResponse("请通过正确渠道访问")
# 导入django内置发送邮件包
#随机数函数
def random_str():
    _str = '1234567890abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(_str) for i in range(4))
 
def email_send(request):
    print('sending')
    email_title = '邮件标题'
    email_body = '邮件内容'
    email =   request.POST.get('email')
    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
    
    if send_status:
        return HttpResponse("成功")
    else:
        return HttpResponse("fail")
def judge_pass(request):
    if request.method =='POST':
        cursor = connection.cursor()
        m_id = request.POST.get('mid')
        pass_no = request.POST.get('pass_no')
        if pass_no == "1":
            cursor.execute("update index_missions set state = 2 where mission_id = {0}".format(m_id))
            return render(request,"home.html")
        else:
            if pass_no == "0":
                cursor.execute("update index_missions set recieve = '' where mission_id = {0}".format(m_id))
                return render(request,"home.html")
            else:
                return HttpResponse("请通过正确渠道访问")
    else:    
        return HttpResponse("请通过正确渠道访问")
