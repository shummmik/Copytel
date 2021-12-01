from django.contrib import admin
from .models import GroupT, NumberT, MessageT, UserT

admin.site.register(GroupT)
admin.site.register(NumberT)
admin.site.register(MessageT)
admin.site.register(UserT)

