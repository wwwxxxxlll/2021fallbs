from django.db import models
class Article(models.Model):
    title = models.CharField(u'标题', max_length = 256)
    content = models.TextField(u'内容')
    time = models.DateTimeField()
class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    ##头像是一个FileField——注意这里必须是“相对路径”，不能是/avatars/这样的绝对路径
    avatar = models.FileField(upload_to='avatars/',default='avatars/default.jpg')
# Create your models here.
