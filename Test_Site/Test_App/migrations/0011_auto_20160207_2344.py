# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-08 06:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test_App', '0010_auto_20160207_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
