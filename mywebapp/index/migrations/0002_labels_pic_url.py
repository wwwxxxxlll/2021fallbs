# Generated by Django 3.2.4 on 2021-12-22 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labels',
            name='pic_url',
            field=models.CharField(default='', max_length=256),
        ),
    ]
