# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 06:48
from __future__ import unicode_literals

import Test_App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_App', '0011_auto_20160207_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to=Test_App.models.user_directory_path),
        ),
    ]
