# Generated by Django 3.1.7 on 2021-07-23 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0012_auto_20210629_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messaget',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='messaget',
            name='video',
        ),
        migrations.DeleteModel(
            name='PhotoT',
        ),
        migrations.DeleteModel(
            name='VideoT',
        ),
    ]
