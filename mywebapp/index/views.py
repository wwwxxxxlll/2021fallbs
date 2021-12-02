from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
import os
import shutil
import json
import cv2

#Create your views here.
def index(request):
    content = [100]
    content.append(20)
    content.append(request.POST.get('video'))
    content2 = 'hello'
    return render(request,"first.html",{'correct':content,'incorrect':content2})
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
            if os.path.splitext(video_name)[1] == ".mp4":   # 筛选mp4文件
                print(video_name)                            # 输出所有的mp4文件
                break

        output_img_path0 = os.path.join('D:\\webapp\\mywebapp\\index\\', 'static',request.user.username)
        output_img_path1 = os.path.join('D:\\webapp\\mywebapp\\index\\', 'static',request.user.username,'image')
        if not os.path.exists(output_img_path0):
            os.mkdir(output_img_path0)
        else:
            # 删除原有目录
            shutil.rmtree(output_img_path0)
            # 创建一个新目录
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
        ps = '/static/'+request.user.username+'/image'+str(i)+'.jpg'
        path1.append(ps)
    return render(request, 'index1.html',{"path1":path1})
@xframe_options_sameorigin
def first(request):
    path1 = ['/static/admin/image1.jpg']
    return render(request,"index1.html",{"cnt_pic":0,'path1':json.dumps(path1)})