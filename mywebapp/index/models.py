from django.db import models
class missions(models.Model):
    states = (
        ('0', '未完成'),
        ('1', '已完成'),
        ('2', '审核中'))
    description = models.CharField(max_length = 256,default = "")
    state = models.CharField(choices=states,max_length = 20,default='未完成', verbose_name='任务状态')
    puber = models.CharField(max_length = 256,default = "")
    recieve = models.CharField(max_length=256,default = "")
    mission_id = models.AutoField(primary_key=True)
    pic_num = models.IntegerField(default=0)
class urls(models.Model):
    pic_url = models.CharField(max_length= 256,default="")
    mission = models.IntegerField(default=0)
class labels(models.Model):
    xMin = models.FloatField(default=0)
    yMin = models.FloatField(default=0)
    height = models.FloatField(default=0)
    width = models.FloatField(default=0)
    label = models.CharField(max_length=256,default="")
    mission = models.IntegerField(default=0)
