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
        self.user_id = 0
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
        # data = [title, ip, login, password, port, ssh, user_id]

        self.table_title = data[0]
        self.user_id = data[-1]

        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.INSERT_SERVER_TABLE, data)


class PeriodOfAction(Database):
    def __init__(self):
        super().__init__()

    def insert_into_period_of_action(self, data):
        # data = [server_url, start_date, end_date, price, user_id]

        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_SERVER_ID, [self.table_title, self.user_id])
            self.table_id = cur.fetchall()[0][0]

            data_lst = [self.table_id] + [elem for elem in data]
            cur.execute(static.INSERT_PERIOD_OF_ACTION, data_lst)


class Operator(ServerTable, PeriodOfAction):
    def __init__(self):
        super().__init__()

    def get_all_titles_and_ips(self, user_id):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_ALL_TITLES, [user_id])
            titles_lst = cur.fetchall()
            titles_lst = [title[0] for title in titles_lst]

            cur.execute(static.GET_ALL_IPs, [user_id])
            ips_lst = cur.fetchall()
            ips_lst = [ip[0] for ip in ips_lst]

            result = {}
            for title, ip in zip(titles_lst, ips_lst):
                result[title] = ip

            return result

    def get_all_info(self, user_id):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_ALL_TITLES, [user_id])
            titles_lst = cur.fetchall()
            titles_lst = [title[0] for title in titles_lst]

            cur.execute(static.GET_ALL_INFO, [user_id, user_id])
            info = cur.fetchall()
            info = [info[0] for info in info]

            final = {}
            for primary_key in titles_lst:
                final[primary_key] = {}

                for key, value in zip(self.table_template, info):
                    final[primary_key][key] = value

            return final

    def get_by_title(self, title, user_id):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_BY_TITLE, [title, user_id, user_id])
            info = list(cur.fetchall()[0])

            final = {}
            for key, value in zip(self.table_template, info):
                final[key] = value

            return final

    def get_by_ip(self, ip, user_id):
        with sq.connect(self.db_name, detect_types=self.args) as con:
            cur = con.cursor()

            cur.execute(static.GET_BY_IP, [ip, user_id, user_id])
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
        # test.get_all_info(277040234)
        pprint(test.get_all_info(277040234))
        print(test.get_by_title('Второе тестирование', 277040234))
        pprint(test.get_by_ip(555, 277040234))
        pprint(test.get_all_titles_and_ips(277040234))
        print('Everything went well')

    except Exception as ex:
        print('Everything went wrong')
        print(ex)


if __name__ == '__main__':
    main()
