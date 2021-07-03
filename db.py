import sql_static as static
import sqlite3 as sq
from datetime import date
from pprint import pprint
from timeit import timeit


class Database:
    def __init__(self):
        self.db_name = static.DB_PATH
        self.args = sq.PARSE_DECLTYPES
        self.table_title = ''
        self.table_id = 0
        self.table_template = ['Title', 'Ip', 'Login', 'Password', 'Port', 'Ssh',
                               'ServerUrl', 'StartDate', 'EndDate', 'Price']

    def init_db(self):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.DROP_SERVER_TABLE)
            cur.execute(static.DROP_PERIOD_OF_ACTION)

            cur.execute(static.CREATE_SERVER_TABLE)
            cur.execute(static.CREATE_PERIOD_OF_ACTION)


class ServerTable(Database):
    def __init__(self):
        super().__init__()

    def insert_into_server_table(self, title, ip, login, password, port, ssh):
        self.table_title = title

        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.INSERT_SERVER_TABLE,
                        (title, ip, login, password, port, ssh))


class PeriodOfAction(Database):
    def __init__(self):
        super().__init__()

    def insert_into_period_of_action(self, server_url, start_date, end_date, price):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_SERVER_ID, [self.table_title])
            self.table_id = cur.fetchall()[0][0]

            cur.execute(static.INSERT_PERIOD_OF_ACTION,
                        (self.table_id, server_url, start_date, end_date, price))


class Operator(ServerTable, PeriodOfAction):
    def __init__(self):
        super().__init__()

    def get_all_info(self):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_ALL_INFO)
            info = cur.fetchall()[0]

            final = {}
            for key, value in zip(self.table_template, info):
                final[key] = value

            return final

    def get_by_title(self, title):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_BY_TITLE, [title])
            info = cur.fetchall()[0]

            final = {}
            for key, value in zip(self.table_template, info):
                final[key] = value

            return final

    def get_by_ip(self, ip):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_BY_IP, [ip])
            info = cur.fetchall()[0]

            final = {}
            for key, value in zip(self.table_template, info):
                final[key] = value

            return final


def main():
    test = Operator()

    try:
        test.init_db()
        test.insert_into_server_table('Title', 420, 'Login', 'Password', 69, 'SSH')
        test.insert_into_period_of_action('URL', date(2021, 7, 3), date(2021, 7, 4), 228)
        test.get_all_info()
        test.get_by_title('Title')
        test.get_by_ip(420)
        print('Everything went well')

    except Exception as ex:
        print('Everything went wrong')
        print(ex)


if __name__ == '__main__':
    main()
