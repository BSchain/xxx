# Generated by Django 2.0 on 2018-04-01 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BSCapp', '0003_notice_if_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modify',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('last_modify_time', models.CharField(max_length=32)),
            ],
        ),
    ]
