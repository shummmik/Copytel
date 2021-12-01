import asyncio
from django.conf import settings
from django.shortcuts import render, HttpResponse
from .models import NumberTForm, NumberT, SmsForm, GroupT, GroupForm
import os
from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetChannelsRequest


async def request_code(mobNumber, apiId, apiHash):
    try:
        client = TelegramClient(os.path.join(settings.SESSIONS_ROOT, str(mobNumber)),
                                apiId,
                                apiHash)
        await client.connect()
        if not await client.is_user_authorized():
            # await client.send_code_request(phone.mobNumber)
            response = await client.send_code_request(mobNumber)
            print(response)
            phone_code_hash = response.phone_code_hash

        session_key = StringSession.save(client.session)
        await client.disconnect()
        return (phone_code_hash, session_key)
    except Exception as ex:
        print(ex)  # delete after logging
        return False




async def reg_code(mobNumber, apiId, apiHash, code, phone_code_hash):
    try:
        client = TelegramClient(os.path.join(settings.SESSIONS_ROOT, str(mobNumber)),
                                apiId,
                                apiHash)
        await client.connect()
        if not await client.is_user_authorized():
            response = await client.sign_in(mobNumber, code, phone_code_hash=phone_code_hash)
            access_hash = response.access_hash
        await client.disconnect()
        return access_hash
    except Exception as ex:
        print(ex)  # delete after logging
        return False


async def get_channel(chat, session_key,  api_id, api_hash):
    async with TelegramClient(StringSession(session_key), api_id, api_hash) as client:
        try:
            result = await client.get_input_entity(chat)

            if type(result) == InputPeerChannel:
                results = await client(GetChannelsRequest(id=[chat]))
                return results.chats[0]
            return None
        except:
            return None


def index(request):
    return render(request, 'base.html')

def addphone(request):
    context = {'header': 'Добавить телефон',
               'title': 'Добавить телефон'}
    if request.method == 'POST':
        form = NumberTForm(request.POST)
        if form.is_valid():
            number = NumberT(mobNumber=form.data['mobNumber'], apiId=form.data['apiId'], apiHash=form.data['apiHash'], user=request.user)
            number.save()
            return HttpResponse('Form saved')#######################################################
        else:
            print(form.errors)
            for i in form.errors.as_data():
                form[i].field.widget.attrs.update(
                    {'class': 'form-control is-invalid'}
                )
            context['formphone'] =  form
    else:
        form = NumberTForm
        context['formphone'] = form
    return render(request, 'formPage.html', context)


def phones(request):
    context = {'header': 'Список телефонов',
               'title': 'Список телефонов'}
    numbers = NumberT.objects.all()
    context['numbers'] = numbers
    return render(request, 'phones.html', context)


def info(request, number):
    context = {'header': 'Info about '+ str(number),
               'title': str(number)}
    number = NumberT.objects.get(mobNumber=number)
    context['number'] = number
    return render(request, 'info.html', context)


def reg(request, number):
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    context = {'header': 'На номер ' + str(number) + 'отправлен запрос для регистрации его в Telegram',
               'title':  'Регистрация номера' + str(number)}
    number = NumberT.objects.get(mobNumber=number)

    if request.method == 'POST':
        form = SmsForm(request.POST)
        if form.is_valid():
            code = form.data['code']
            answer_reg_code = loop.run_until_complete(reg_code(
                number.mobNumber,
                number.apiId,
                number.apiHash,
                code,
                number.phone_code_hash
            ))
            if answer_reg_code:
                number.access_hash = answer_reg_code
                number.registration = True
                number.save(update_fields=['access_hash', 'registration'])
                # form.save()
                context['content'] = 'Все прошло отлично. Работаем дальше'
                return render(request, 'clear.html', context)
            else:
                context['content'] = 'Error in reg code'
                return render(request, 'clear.html', context)
        else:
            print(form.errors)
            for i in form.errors.as_data():
                form[i].field.widget.attrs.update(
                    {'class': 'form-control is-invalid'})
            context['formphone'] = form
    else:
        answer_request_code = loop.run_until_complete(request_code(
                number.mobNumber,
                number.apiId,
                number.apiHash
            ))
        if answer_request_code:
            phone_code_hash, session_key = answer_request_code
            number.phone_code_hash = phone_code_hash
            number.session_key = session_key
            number.save(update_fields=['phone_code_hash', 'session_key'])
        else:
            context['content'] = 'Error in send code'
            return render(request, 'clear.html', context)
        form = SmsForm
        context['formphone'] = form
    loop.close()
    return render(request, 'formPage.html', context)


def chanels(request, number):
    context = {'header': 'Список групп номера: {}'.format(number),
               'title': 'Список групп номера: {}'.format(number)}
    numberT = NumberT.objects.get(mobNumber=number)
    groups = GroupT.objects.filter(numberT=numberT)
    context['groups'] = groups
    context['number'] = number
    return render(request, 'groups.html', context)


def add_group(request, number):
    context = {'header': 'Добавление группы к номеру: {}'.format(number),
               'title': 'Добавление группы к номеру: {}'.format(number)}
    if request.method == 'POST':

        form = GroupForm(request.POST)
        if form.is_valid():
            number = NumberT.objects.get(mobNumber=number)
            loop = asyncio.new_event_loop()
            group = loop.run_until_complete(get_channel(request.POST['name'],
                                                        number.session_key,
                                                        number.apiId,
                                                        number.apiHash)
                                            )
            if group:
                if GroupT.objects.filter(IdT=group.id).exists():
                    context['content'] = 'Такая группа уже есть'
                    return render(request, 'clear.html', context)
                else:
                    groupt = GroupT(name=group.username, title=group.title, dateT=group.date, IdT=group.id, numberT=number)
                    groupt.save()
                    context['content'] = 'Группа {} добавлена'.format(group.username)
                    return render(request, 'clear.html', context)
        else:
            print(form.errors)
            for i in form.errors.as_data():
                form[i].field.widget.attrs.update({'class': 'form-control is-invalid'})
            context['formphone'] =  form
    else:
        form = GroupForm
        context['formphone'] = form
    return render(request, 'formPage.html', context)