# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-09 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_auditlog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auditlog',
            options={'managed': False},
        ),
    ]
