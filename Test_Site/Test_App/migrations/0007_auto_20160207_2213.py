# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 05:13
from __future__ import unicode_literals

import Test_App.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_App', '0006_uploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to=Test_App.models.generate_filename),
        ),
    ]
