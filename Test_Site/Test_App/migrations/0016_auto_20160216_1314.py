# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 20:14
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Test_App', '0015_auto_20160210_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_description', models.TextField(verbose_name=b'Project Description')),
                ('name', models.CharField(max_length=200, verbose_name=b'Project Name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectWall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.date.today)),
                ('entry', models.TextField(verbose_name=b'Entry')),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Test_App.Project')),
            ],
        ),
        migrations.CreateModel(
            name='UserFileDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name=b'A text Description')),
            ],
        ),
        migrations.CreateModel(
            name='UserFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200, verbose_name=b'Location on Disk')),
                ('url', models.CharField(max_length=200, verbose_name=b'URL of the file')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userfiledescription',
            name='resource',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Test_App.UserFiles'),
        ),
    ]
