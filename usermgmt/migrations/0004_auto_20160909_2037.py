# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 20:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0003_auto_20160909_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='registration_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='usermgmt.RegistrationCode'),
        ),
    ]
