from telethon.sessions import StringSession
from telethon import TelegramClient, events
from pathlib import Path
import os
import json
import datetime
import redis
import uuid
from settings import HOST, PORT_R, DB_R, NEW_MESSAGE, EDIT_MESSAGE, DELETE_MESSAGE

redis_client = redis.Redis(HOST, PORT_R, DB_R)
BASE_DIR = os.path.join(Path(__file__).resolve().parent.parent, 'media')


def date_format(message):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(message, (datetime.datetime, datetime.date)):
        return message.isoformat()
    if isinstance(message, (bytes)):
        return str(message)
    raise TypeError("Type %s not serializable" % type(message))


################################################
offset = 42
limit = 100
################################################


def startsession(session_key, api_id, api_hash):
    client = TelegramClient(StringSession(session_key),
                            api_id,
                            api_hash,
                            # loop=loop,
                            )

    @client.on(events.MessageDeleted())
    async def my_event_deleted(event):
        redis_client.lpush(
            DELETE_MESSAGE,
            json.dumps(event.original_update.to_dict())
        )

    @client.on(events.MessageEdited())
    async def my_event_edit(event):
        redis_client.lpush(
            EDIT_MESSAGE,
            json.dumps(event.message.to_dict(), default=date_format)
        )

    @client.on(events.NewMessage())
    async def my_event_create(event):

        redis_client.lpush(
            NEW_MESSAGE,
            json.dumps(event.message.to_dict(), default=date_format)
        )
        if event.message.photo:
            uid = uuid.uuid4()
            await event.message.download_media(
                file=os.path.join(BASE_DIR,
                                  'image',
                                  event.message.date.strftime('%Y/%m/%d'), '.'
                                  )
            )
            print(json.loads('{messsage_id: %d, channel_id: %d, path: \"%s\"}'
                             % (event.message['id'],
                                event.message['peer_id']['channel_id'],
                                uid)))
            return;
        elif event.message.video:
            await event.message.download_media(
                file=os.path.join(BASE_DIR,
                                  'video',
                                  event.message.date.strftime('%Y/%m/%d'), '.'
                                  )
            )
            return;
        elif event.message.audio:
            await event.message.download_media(
                file=os.path.join(BASE_DIR,
                                  'audio',
                                  event.message.date.strftime('%Y/%m/%d'), '.'
                                  )
            )
            return;
        elif event.message.voice:
            await event.message.download_media(
                  file=os.path.join(BASE_DIR,
                                  'voice',
                                  event.message.date.strftime('%Y/%m/%d'), '.'
                                  )
            )
            return;
        if event.message.document:
            await event.message.download_media(
                file=os.path.join(BASE_DIR,
                                  'document',
                                  event.message.date.strftime('%Y/%m/%d'), '.'
                                  )
            )
            return;

    client.start()
    client.run_until_disconnected()
    # return client
