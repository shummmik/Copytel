import time
from multiprocessing import Process
from onlinesession import startsession
from settings import HOST, PORT_P, DB_P, PASSWORD_P, USER_P
from sqlalchemy import Table, Column, MetaData, BigInteger, create_engine

db_string = "postgresql://{}:{}@{}:{}/{}".format(USER_P, PASSWORD_P, HOST, PORT_P, DB_P)


class ProcessSession(Process):
    def __init__(self, name, session_key, api_id, api_hash):
        Process.__init__(self)
        self.session_key = session_key
        self.api_id = api_id
        self.api_hash = api_hash
        self.name = name

    def run(self):
        try:
            startsession(self.session_key, self.api_id, self.api_hash)
        except Exception as ex:
            print('process {} is dead'.format(self.name))
            print(ex)
        print('stop {}'.format(self.name))


class ManagerSessions:
    def __init__(self, dbstring, app_name):
        self.app_name = app_name
        self.processes = {}
        self.phone_session = []
        self.db_string = dbstring
        self.engine = create_engine(self.db_string, connect_args={"application_name": app_name})

    def start(self):
        while True:
            self.update_list_sessions()
            self.update_sessions()
            time.sleep(300)

    def add_process(self, name, session_key, api_id, api_hash):
        new_process = ProcessSession(str(name), session_key, api_id, api_hash)
        new_process.start()
        self.processes[name] = new_process

    def remove_process(self, name):
        self.processes[name].terminate()
        self.processes[name].join()

    def update_list_sessions(self):
        numbers_work = list(self.processes.keys())
        numbers_bd = self.get_numbers()
        for number_bd in numbers_bd:
            if number_bd['mobNumber'] in numbers_work:
                numbers_work.remove(number_bd['mobNumber'])
            else:
                self.add_process(number_bd['mobNumber'],
                                 number_bd['session_key'],
                                 number_bd['apiId'],
                                 number_bd['apiHash'])
        for number_work in numbers_work:
            self.remove_process(number_work)

    def update_sessions(self):
        for process in list(self.processes.keys()):
            if not self.processes[process].is_alive():
                print('Поток {} умер, перезапускаем'.format(process))
                new_process = ProcessSession(self.processes[process].name,
                                             self.processes[process].session_key,
                                             self.processes[process].api_id,
                                             self.processes[process].api_hash
                                             )
                self.processes[process].join()
                self.processes[process] = new_process
                self.processes[process].start()

    def get_numbers(self):
        return self.engine.execute(
            """SELECT \"mobNumber\", \"apiId\", \"apiHash\", \"session_key\" 
                FROM public.groups_numbert 
                where registration = true""")


if __name__ == "__main__":
    session_manager = ManagerSessions(db_string, 'ListenTelegram')
    session_manager.start()
