# Generated by Django 3.1.7 on 2021-05-25 12:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20210518_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='photot',
            name='path',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='videot',
            name='path',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='numbert',
            name='mobNumber',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator('^(\\d{7,})$', message='Not a number or a short one')]),
        ),
    ]
