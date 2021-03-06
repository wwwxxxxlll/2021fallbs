# Generated by Django 3.2.4 on 2021-12-05 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20211205_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
