# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 03:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BSCapp', '0002_auto_20180124_1017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transcation',
            new_name='Transaction',
        ),
    ]
