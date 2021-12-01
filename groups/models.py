from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime
from django import forms
import uuid

# Create your models here.
User = get_user_model()

# ссылка!!!!!!!!!!!!!!!!!!!!
class NumberT(models.Model):
    mobNumber = models.BigIntegerField(validators=[RegexValidator(regex='^(\d{9,14})$', message="Not a number or a short one")], unique=True)
    apiId = models.IntegerField(validators=[RegexValidator(regex='^(\d{7})$', message="Not a number or a short one")])
    apiHash = models.CharField(max_length=40)
    session_key = models.CharField(max_length=360, null=True)
    phone_code_hash = models.CharField(max_length=20, null=True)
    access_hash = models.CharField(max_length=20, null=True)
    registration = models.BooleanField(default=False)
    # group for access
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='numbers_user')

    def __str__(self):
        return str(self.mobNumber)


class GroupT(models.Model):
    IdT = models.TextField()
    name = models.CharField(max_length=40)
    title = models.CharField(max_length=400, null=True)
    description = models.TextField(null=True)
    dateT = models.DateTimeField(default=datetime.now)
    numberT = models.ForeignKey(NumberT, on_delete=models.SET_NULL, null=True, related_name='groups_number')
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class UserT(models.Model):
    USER = 0
    ATCHAT = 1
    BOT = 2
    ATTRIBUTE_CHOICES = [
        (USER, 'User'),
        (ATCHAT, 'atChat'),
        (BOT, 'Bot'),
    ]
    idT = models.IntegerField(unique=True, db_index=True)
    userName = models.CharField(max_length=100, null=True)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    userType = models.IntegerField(choices=ATTRIBUTE_CHOICES, default=USER)


class MessageT(models.Model):
    text = models.TextField()
    userT = models.ForeignKey(UserT, on_delete=models.SET_NULL, null=True)
    # photo = models.ForeignKey(PhotoT, on_delete=models.SET_NULL, null=True)
    # video = models.ForeignKey(VideoT, on_delete=models.SET_NULL, null=True)
    # date = models.DateTimeField()
    dateT = models.DateTimeField()
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)


class PhotoT(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    idT = models.IntegerField()
    dateT = models.DateTimeField(default=datetime.now)
    # format = models.CharField(max_length=5)
    uid = models.UUIDField()
    path = models.CharField(max_length=260, null=True)
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)
    messageT = models.ForeignKey(MessageT, on_delete=models.CASCADE, null=True)


class VideoT(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    idT = models.IntegerField()
    dateT = models.DateTimeField(default=datetime.now)
    # format = models.CharField(max_length=5)
    uid = models.UUIDField()
    path = models.CharField(max_length=260, null=True)
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)
    messageT = models.ForeignKey(MessageT, on_delete=models.CASCADE, null=True)


class AudioT(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    idT = models.IntegerField()
    dateT = models.DateTimeField(default=datetime.now)
    # format = models.CharField(max_length=5)
    uid = models.UUIDField()
    path = models.CharField(max_length=260, null=True)
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)
    messageT = models.ForeignKey(MessageT, on_delete=models.CASCADE, null=True)


class VoiceT(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    idT = models.IntegerField()
    dateT = models.DateTimeField(default=datetime.now)
    # format = models.CharField(max_length=5)
    uid = models.UUIDField()
    path = models.CharField(max_length=260, null=True)
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)
    messageT = models.ForeignKey(MessageT, on_delete=models.CASCADE, null=True)


class DocumentT(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    idT = models.IntegerField()
    dateT = models.DateTimeField(default=datetime.now)
    # format = models.CharField(max_length=5)
    uid = models.UUIDField()
    path = models.CharField(max_length=260, null=True)
    groupT = models.ForeignKey(GroupT, on_delete=models.CASCADE, null=True)
    messageT = models.ForeignKey(MessageT, on_delete=models.CASCADE, null=True)


class NumberTForm(forms.ModelForm):
    class Meta:
        model = NumberT
        fields = ['mobNumber', 'apiId', 'apiHash']
        widgets = {
            'mobNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
            'apiId': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter apiId'}),
            'apiHash': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter apiHash'}),
            # error_messages = {'invalid': 'Enter a valid mobile number',
            #                   'required': 'Enter a valid mobile number'}
        }
        labels = {
            'mobNumber': ('Мобильный номер'),
        }
        help_texts = {
            'mobNumber': ('Должен содержать только цифры'),
        }
        error_messages = {
            'mobNumber': {
                'max_length': ("This writer's name is too long."),
            },
        }
        forms.BoundField

class SmsForm(forms.Form):
    code = forms.IntegerField(label='Verify code', max_value=99999)

class GroupForm(forms.Form):
    name = forms.CharField(label='Введите название группы')