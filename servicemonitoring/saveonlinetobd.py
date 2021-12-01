import json
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Table, Column, MetaData, BigInteger, create_engine
from settings import HOST, PORT_P, DB_P,  PASSWORD_P, USER_P, PORT_R, DB_R
from settings import NEW_MESSAGE, EDIT_MESSAGE, DELETE_MESSAGE, HISTORY_MESSAGE
from settings import NEW_MESSAGE_P, EDIT_MESSAGE_P, DELETE_MESSAGE_P, HISTORY_MESSAGE_P
import redis
import time

redis_client = redis.Redis(HOST, PORT_R, DB_R)
metadata = MetaData()


db_string = "postgresql://{}:{}@{}:{}/{}".format(USER_P, PASSWORD_P, HOST, PORT_P, DB_P)

engine = create_engine(db_string, connect_args={"application_name": "SaveOnlineDB"})


def get_table(table):
    return Table(
        table, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('message', JSONB)
    )


table_meta_new = Table(
        NEW_MESSAGE_P, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('message', JSONB)
    )


table_meta_del = Table(
        DELETE_MESSAGE_P, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('message', JSONB)
    )


table_meta_edit = Table(
        EDIT_MESSAGE_P, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('message', JSONB)
    )

table_meta_his = Table(
        HISTORY_MESSAGE_P, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('message', JSONB)
    )


def get_from_redis(table, count=10):
    len_new = redis_client.llen(table)
    values = []
    if len_new != 0:
        for i in range(len_new if len_new <= count else count):
            val = json.loads(redis_client.rpop(table).decode('utf-8'))
            values.append(val)
        return values
    return None


def return_meta(table):
    if table == NEW_MESSAGE_P:
        # print('new')
        return table_meta_new
    if table == EDIT_MESSAGE_P:
        # print('edit')
        return table_meta_edit
    if table == DELETE_MESSAGE_P:
        # print('del')
        return table_meta_del
    if table == HISTORY_MESSAGE_P:
        return table_meta_his


def insert_to_postgres(table_p, table_r, connect):
    values = get_from_redis(table_r)
    if values:
        table_meta = return_meta(table_p)
        for value in values:
            connect.execute(
                table_meta.insert(),
                message=value
            )


with engine.connect() as conn:
    while True:
        with conn.begin():
            insert_to_postgres(NEW_MESSAGE_P, NEW_MESSAGE, conn)
        with conn.begin():
            insert_to_postgres(EDIT_MESSAGE_P, EDIT_MESSAGE, conn)
        with conn.begin():
            insert_to_postgres(DELETE_MESSAGE_P, DELETE_MESSAGE, conn)
        with conn.begin():
            insert_to_postgres(HISTORY_MESSAGE_P, HISTORY_MESSAGE, conn)
        time.sleep(10)
