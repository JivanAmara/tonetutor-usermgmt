# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationcode',
            name='subscription_required',
            field=models.BooleanField(default=True),
        ),
    ]
