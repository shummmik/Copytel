# Generated by Django 3.1.7 on 2021-04-19 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idT', models.IntegerField()),
                ('format', models.TextField(verbose_name=5)),
                ('uid', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='UserT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idT', models.IntegerField()),
                ('userName', models.TextField(verbose_name=20)),
                ('description', models.TextField(verbose_name=100)),
            ],
        ),
        migrations.CreateModel(
            name='VideoT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idT', models.IntegerField()),
                ('format', models.TextField(verbose_name=5)),
                ('uid', models.UUIDField()),
            ],
        ),
        migrations.AddField(
            model_name='groupt',
            name='description',
            field=models.TextField(default='Not null', verbose_name=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupt',
            name='name',
            field=models.TextField(default='group', verbose_name=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='number',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('dateT', models.DateTimeField()),
                ('groupT', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.groupt')),
                ('photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.photot')),
                ('userT', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.usert')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='groups.videot')),
            ],
        ),
    ]