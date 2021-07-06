from db import Operator
from bot_token import TOKEN
from telegram.ext import Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import date
import emoji


class ServerBot:
    def __init__(self):
        self.token = TOKEN

        # initializing the stages vars
        self.INLINE_CHOOSING = 1
        self.TITLES_IP_STAGE = 2
        self.RECORD_CREATING = 3
        self.GETTING_BY_TITLE = 4
        self.GETTING_BY_IP = 5

        # initializing the callback data vars
        self.CREATE_A_RECORD, self.RETURN_TO_START = 1, 1
        self.GET_ALL_RECORDS = 2
        self.GET_RECORD_BY_TITLE = 3
        self.GET_RECORD_BY_IP = 4

    @staticmethod
    def fix_server_info(data):
        result = ''
        length = len(data.keys()) + 1

        for square, key in zip(range(1, length), data.keys()):
            if square % 2 == 0:
                square = '◾'
            else:
                square = '◽'
            result += f'{square}{key}: {data[key]};\n'

        return result

    @staticmethod
    def fix_time(wrong_time):
        wrong_time = wrong_time.split('-')
        wrong_time = [int(elem) for elem in wrong_time]

        return date(wrong_time[0], wrong_time[1], wrong_time[2])

    @staticmethod
    def replace_num(string):
        letters_dict = {'0': emoji.emojize(':keycap_0:'), '1': emoji.emojize(':keycap_1:'),
                        '2': emoji.emojize(':keycap_2:'), '3': emoji.emojize(':keycap_3:'),
                        '4': emoji.emojize(':keycap_4:'), '5': emoji.emojize(':keycap_5:'),
                        '6': emoji.emojize(':keycap_6:'), '7': emoji.emojize(':keycap_7:'),
                        '8': emoji.emojize(':keycap_8:'), '9': emoji.emojize(':keycap_9:'),
                        '10': emoji.emojize(':keycap_10:'), '!': emoji.emojize(':red_exclamation_mark:')}

        new_string = ''
        for elem in string:
            if elem not in list(letters_dict.keys()):
                new_string += elem
            elif elem in list(letters_dict.keys()):
                new_string += letters_dict[elem]

        return new_string

    def fix_titles_ips(self, data):
        result = ''
        length = range(1, len(data.keys()) + 1)

        for number, title in zip(length, data.keys()):
            result += f'{self.replace_num(str(number))} Название: {title}; IP: {data[title]}\n'

        return result[:-1]

    def start(self, update, context):
        keyboard = [
            [InlineKeyboardButton('Добавить запись', callback_data=str(self.CREATE_A_RECORD))],
            [InlineKeyboardButton('Получить названия & ip всех записей', callback_data=str(self.GET_ALL_RECORDS))],
            [InlineKeyboardButton('Получить запись по названию', callback_data=str(self.GET_RECORD_BY_TITLE))],
            [InlineKeyboardButton('Получить запись по ip', callback_data=str(self.GET_RECORD_BY_IP))]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Я помогу сохранить данные о вашем сервере',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Просто выберете одну из опций:', reply_markup=reply_markup)

        return self.INLINE_CHOOSING

    def start_over(self, update, context):
        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        keyboard = [
            [InlineKeyboardButton('Добавить запись', callback_data=str(self.CREATE_A_RECORD))],
            [InlineKeyboardButton('Получить названия & ip всех записей', callback_data=str(self.GET_ALL_RECORDS))],
            [InlineKeyboardButton('Получить запись по названию', callback_data=str(self.GET_RECORD_BY_TITLE))],
            [InlineKeyboardButton('Получить запись по ip', callback_data=str(self.GET_RECORD_BY_IP))]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text('Выберете одну из опций:', reply_markup=reply_markup)

        return self.INLINE_CHOOSING

    def create_a_record(self, update, context):
        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        keyboard = [
            ['Вернуться к началу'],
            ['Пример записи']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        query.edit_message_text("Создаем новую запись")

        text_for_user = 'Вы можете сохранить следующие данные о сервере:\n1 Название сервера\n2 IP сервера\n' \
                        '3 Логин от вашего сервера\n4 Пароль от вашего сервера\n5 Используемый порт\n6 SSH\n7 ' \
                        'Url-ссылка на ваш сервер\n8 Дата начала периода оплаты\n9 Дата конца периода оплаты\n' \
                        '10 Цена периода аренды'
        text_for_user = self.replace_num(text_for_user)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_for_user)

        text_for_user = "! Если поле вам не требуется, вы можете поставить '-'\n" \
                        "! Дата обязательно должна быть записана в следующем формате: 'year-month-day'\n" \
                        "! Запись должна идти в строку, данные должны быть разделены запятой и пробелом"
        text_for_user = self.replace_num(text_for_user)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_for_user,
                                 reply_markup=reply_markup)

        return self.RECORD_CREATING

    def write_down_data(self, update, context):
        data = update.message.text

        try:
            data = data.split(', ')
            data[-3] = self.fix_time(data[-3])
            data[-2] = self.fix_time(data[-2])

            operator = Operator()

            operator.insert_into_server_table(data[:6])
            operator.insert_into_period_of_action(data[6:])

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Запись сохранена')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            ['Вернуться к началу'],
            ['Пример записи']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Вам надо ввести данные в следующем формате:\n"
                                      "'title, ip, login, password, port, ssh, "
                                      "server_url, start_date, end_date, price'",
                                 reply_markup=reply_markup)

        return self.RECORD_CREATING

    def help(self, update, context):
        keyboard = [
            ['Вернуться к началу'],
            ['Пример записи']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        text_for_user = 'Сервер А, 212.232.79.129, @flexxx, ghslKBDdig4772, 1024, {user}@{host}, ' \
                        'www.damn.com, 2021-07-06, 2021-07-07, 420$'

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_for_user,
                                 reply_markup=reply_markup)

        return self.RECORD_CREATING

    def get_all_records(self, update, context):
        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        keyboard = [
            [InlineKeyboardButton('Получить запись по названию', callback_data=str(self.GET_RECORD_BY_TITLE))],
            [InlineKeyboardButton('Получить запись по ip', callback_data=str(self.GET_RECORD_BY_IP))],
            [InlineKeyboardButton('К началу', callback_data=str(self.RETURN_TO_START))]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        db_operator = Operator()
        titles_ips = db_operator.get_all_titles_and_ips()
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}',
                                reply_markup=reply_markup)

        return self.TITLES_IP_STAGE

    def get_record_by_title(self, update, context):
        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        db_operator = Operator()
        titles_ips = db_operator.get_all_titles_and_ips()
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}')

        keyboard = [
            ['Вернуться к началу']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите название сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_TITLE

    def get_by_title_db(self, update, context):
        server_title = update.message.text

        try:
            operator = Operator()
            result = operator.get_by_title(server_title)
            result = self.fix_server_info(result)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Об этом сервере мне известно следующее:\n{result}')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            ['Вернуться к началу']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите название сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_TITLE

    def get_record_by_ip(self, update, context):
        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        db_operator = Operator()
        titles_ips = db_operator.get_all_titles_and_ips()
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}')

        keyboard = [
            ['Вернуться к началу']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите IP сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_IP

    def get_by_ip_db(self, update, context):
        server_ip = update.message.text
        print(server_ip)

        try:
            operator = Operator()
            result = operator.get_by_ip(server_ip)
            result = self.fix_server_info(result)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Об этом сервере мне известно следующее:\n{result}')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            ['Вернуться к началу']
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите IP сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_IP

    def run(self):
        updater = Updater(self.token)
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.INLINE_CHOOSING: [
                    CallbackQueryHandler(self.create_a_record, pattern='^' + str(self.CREATE_A_RECORD) + '$'),
                    CallbackQueryHandler(self.get_all_records, pattern='^' + str(self.GET_ALL_RECORDS) + '$'),
                    CallbackQueryHandler(self.get_record_by_title, pattern='^' + str(self.GET_RECORD_BY_TITLE) + '$'),
                    CallbackQueryHandler(self.get_record_by_ip, pattern='^' + str(self.GET_RECORD_BY_IP) + '$')
                ],
                self.TITLES_IP_STAGE: [
                    CallbackQueryHandler(self.get_record_by_title, pattern='^' + str(self.GET_RECORD_BY_TITLE) + '$'),
                    CallbackQueryHandler(self.get_record_by_ip, pattern='^' + str(self.GET_RECORD_BY_IP) + '$'),
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$')
                ],
                self.RECORD_CREATING: [
                    MessageHandler(Filters.regex('^Вернуться к началу$'), self.start),
                    MessageHandler(Filters.regex('^Пример записи$'), self.help),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу | Пример записи$'),
                                   self.write_down_data)
                ],
                self.GETTING_BY_TITLE: [
                    MessageHandler(Filters.regex('^Вернуться к началу$'), self.start),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу$'), self.get_by_title_db)
                ],
                self.GETTING_BY_IP: [
                    MessageHandler(Filters.regex('^Вернуться к началу$'), self.start),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу$'), self.get_by_ip_db)
                ]
            },
            fallbacks=[CommandHandler('start', self.start)]
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()


def main():
    test = ServerBot()
    test.run()


if __name__ == '__main__':
    main()
