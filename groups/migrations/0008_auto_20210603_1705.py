# Generated by Django 3.1.7 on 2021-06-03 14:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0007_auto_20210527_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='numbert',
            name='access_hash',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='numbert',
            name='phone_code_hash',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='numbert',
            name='registration',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='numbert',
            name='mobNumber',
            field=models.IntegerField(unique=True, validators=[django.core.validators.RegexValidator(message='Not a number or a short one', regex='^(\\d{9,14})$')]),
        ),
        migrations.AlterField(
            model_name='numbert',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='auth.user'),
            preserve_default=False,
        ),
    ]
