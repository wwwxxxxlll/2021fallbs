from django.db import connection, connections
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import  login,logout
from django.contrib import auth
import os
import shutil
import json
import pymysql
import cv2
from django.conf import settings
from index.models import missions


#Create your views here.
def index(request):
    content = [100]
    content.append(20)
    content.append(request.POST.get('video'))
    content2 = 'hello'
    return render(request,"video.html",{'correct':content,'incorrect':content2})
def upload(request):                      # 设置路径
    if request.method == 'POST':# 获取对象
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
    path1 = []
    for i in range(1,cnt_pic+1):
        ps = '/static/pic/'+request.user.username+'/'+os.path.splitext(obj.name)[0]+'image'+str(i)+'.jpg'
        path1.append(ps)
    return render(request, 'index1.html',{"path1":path1})

def pub_pic(request):
    if request.method == 'POST':
        # 获取 上传的 图片信息
        img = request.FILES.get('img')

        # 获取上传图片的名称
        img_name = img.name

        if not os.path.exists(os.path.join(os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username))):
                os.mkdir(os.path.join(os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username)))
        img_path = os.path.join('D:\\webapp\\mywebapp\\index\\static\\pic',request.user.username, img_name)

        # 写入 上传图片的 内容
        with open(img_path, 'ab') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        cursor = connection.cursor()
        description = request.POST.get('description')
        puber = request.user.username
        state = '0'
        pic_num = 1
        path1 = '/static/pic/'+puber+'/'+os.path.splitext(img_name)[0]+os.path.splitext(img_name)[1]
        m = missions.objects.create(description = description,puber=puber,state=state,pic_num=pic_num)
        cursor.execute("insert into index_urls(pic_url,mission)values('{0}',{1})".format(path1,m.mission_id))
        return render(request,"pic.html",{"path1":path1})
    else:
        return render(request,"pic.html")
def home(request):
    return render(request,"home.html")
def reg(request):
    return render(request,"reg.html")
def register(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        name = request.POST.get('username')
        psswd = request.POST.get('password')
        e_mail = request.POST.get('email')
        cursor.execute("select * from auth_user where username='%s'"%(name))
        count = cursor.fetchall()
        if(count == ()):
            User.objects.create_user(username=name,password=psswd,email= e_mail)
            return render(request,"home.html")
        else:
            return HttpResponse("重复用户名")
def sign_in(request):
    return render(request,"signin.html")
def signin(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(username=name, password=password)
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
        return
    return
def mission_pub_pic(request):
    cursor = connection.cursor()

    return