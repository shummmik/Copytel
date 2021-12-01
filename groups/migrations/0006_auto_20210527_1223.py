# Generated by Django 3.1.7 on 2021-05-27 09:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20210525_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numbert',
            name='mobNumber',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator(message='Not a number or a short one', regex='^(\\d{9,})$')]),
        ),
    ]
