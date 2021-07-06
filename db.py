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

    def insert_into_server_table(self, data):
        # data = [title, ip, login, password, port, ssh]

        self.table_title = data[0]

        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.INSERT_SERVER_TABLE, data)


class PeriodOfAction(Database):
    def __init__(self):
        super().__init__()

    def insert_into_period_of_action(self, data):
        # data = [server_url, start_date, end_date, price]

        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_SERVER_ID, [self.table_title])
            self.table_id = cur.fetchall()[0][0]

            data_lst = [self.table_id] + [elem for elem in data]
            cur.execute(static.INSERT_PERIOD_OF_ACTION, data_lst)


class Operator(ServerTable, PeriodOfAction):
    def __init__(self):
        super().__init__()

    def get_all_titles_and_ips(self):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_ALL_TITLES)
            titles_lst = cur.fetchall()
            titles_lst = [title[0] for title in titles_lst]

            cur.execute(static.GET_ALL_IPs)
            ips_lst = cur.fetchall()
            ips_lst = [ip[0] for ip in ips_lst]

            result = {}
            for title, ip in zip(titles_lst, ips_lst):
                result[title] = ip

            return result

    def get_all_info(self):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_ALL_TITLES)
            titles_lst = cur.fetchall()[0]

            cur.execute(static.GET_ALL_INFO)
            info = cur.fetchall()[0]

            final = {}
            for primary_key in titles_lst:
                final[primary_key] = {}

                for key, value in zip(self.table_template, info):
                    final[primary_key][key] = value

            return final

    def get_by_title(self, title):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_BY_TITLE, [title])
            info = list(cur.fetchall()[0])

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
        # test.init_db()
        # test.insert_into_server_table(['Title', 420, 'Login', 'Password', 69, 'SSH'])
        # test.insert_into_period_of_action(['URL', date(2021, 7, 3), date(2021, 7, 4), 228])
        # test.get_all_info()
        # pprint(test.get_all_info())
        # print(test.get_by_title('Второе тестирование'))
        test.get_by_ip(555)
        # test.get_all_titles_and_ips()
        print('Everything went well')

    except Exception as ex:
        print('Everything went wrong')
        print(ex)


if __name__ == '__main__':
    main()
