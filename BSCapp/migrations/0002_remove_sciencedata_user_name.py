# Generated by Django 2.0 on 2018-07-06 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BSCapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sciencedata',
            name='user_name',
        ),
    ]
