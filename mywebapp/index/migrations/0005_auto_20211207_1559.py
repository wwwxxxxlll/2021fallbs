# Generated by Django 3.2.4 on 2021-12-07 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20211205_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='labels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xMin', models.FloatField(default=0)),
                ('yMin', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('width', models.FloatField(default=0)),
                ('label', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='missions',
            fields=[
                ('description', models.CharField(default='', max_length=256)),
                ('state', models.CharField(choices=[('0', '未完成'), ('1', '已完成'), ('2', '审核中')], default='未完成', max_length=20, verbose_name='任务状态')),
                ('puber', models.CharField(default='', max_length=256)),
                ('recieve', models.CharField(default='', max_length=256)),
                ('mission_id', models.IntegerField(primary_key=True, serialize=False)),
                ('pic_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='urls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_url', models.CharField(default='', max_length=256)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.missions')),
            ],
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='labels',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.missions'),
        ),
    ]
