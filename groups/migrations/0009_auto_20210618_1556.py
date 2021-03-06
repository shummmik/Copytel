# Generated by Django 3.1.7 on 2021-06-18 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_auto_20210603_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupt',
            name='dateT',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='groupt',
            name='title',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='groupt',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
