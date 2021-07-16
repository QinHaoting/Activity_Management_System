# Generated by Django 3.1.7 on 2021-07-16 01:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sac_app', '0004_activities_org_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='bbs_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bbs_id', models.CharField(max_length=64)),
                ('bbs_message', models.TextField()),
                ('bbs_create_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='org_directMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_id', models.CharField(max_length=64)),
                ('message', models.TextField()),
                ('accept_id', models.CharField(max_length=64)),
                ('message_send_time', models.DateTimeField(default=datetime.datetime.now)),
                ('message_valid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='stu_directMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_id', models.CharField(max_length=64)),
                ('message', models.TextField()),
                ('accept_id', models.CharField(max_length=64)),
                ('message_send_time', models.DateTimeField(default=datetime.datetime.now)),
                ('message_valid', models.IntegerField()),
            ],
        ),
    ]
