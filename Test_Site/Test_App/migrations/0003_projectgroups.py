# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 22:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Test_App', '0002_userextensiononetoone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'NIST', max_length=20, verbose_name=b'Group Name')),
                ('people', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
