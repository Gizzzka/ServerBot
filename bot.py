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

        # saving the user id
        self.user_id = 0

        # making update instance
        self.update = None

        # initializing the stages vars
        self.INLINE_CHOOSING = 1
        self.TITLES_IP_STAGE = 2
        self.GETTING_BY_TITLE = 3
        self.GETTING_BY_IP = 4
        self.RECORD_CREATING = 5

        # initializing the stages var for collecting_data
        self.COLLECTING_THE_TITLE = 6
        self.COLLECTING_THE_IP = 7
        self.COLLECTING_THE_LOGIN = 8
        self.COLLECTING_THE_PASSWORD = 9
        self.COLLECTING_THE_PORT = 10
        self.COLLECTING_THE_SSH = 11
        self.COLLECTING_THE_URL = 12
        self.COLLECTING_THE_START_DATE = 13
        self.COLLECTING_THE_END_DATE = 14
        self.COLLECTING_THE_PRICE = 15

        # initializing the callback data vars
        self.CREATE_A_RECORD, self.RETURN_TO_START = 1, 1
        self.GET_ALL_RECORDS, self.COLLECTING_DATA = 2, 2
        self.GET_RECORD_BY_TITLE = 3
        self.GET_RECORD_BY_IP = 4

        # initializing the server_data var
        self.server_data = []

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

        self.update = query.edit_message_text('Выберете одну из опций:', reply_markup=reply_markup)

        message_id = self.update.message_id

        for num in range(-message_id, 1):
            try:
                message_id -= 1
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
            except Exception as ex:
                print(ex)
                break

        return self.INLINE_CHOOSING

    def create_a_record(self, update, context):
        # getting the user id
        self.user_id = update.effective_user.id

        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        text_for_user = 'Вы можете сохранить следующие данные о сервере:\n1 Название сервера\n2 IP сервера\n' \
                        '3 Логин от вашего сервера\n4 Пароль от вашего сервера\n5 Используемый порт\n6 SSH\n7 ' \
                        'Url-ссылка на ваш сервер\n8 Дата начала периода оплаты\n9 Дата конца периода оплаты\n' \
                        '10 Цена периода аренды'
        text_for_user = self.replace_num(text_for_user)

        self.update = query.edit_message_text(text_for_user)

        message_id = self.update.message_id

        text_for_user = "! Если поле вам не требуется, вы можете поставить '-'\n" \
                        "! Дата обязательно должна быть записана в следующем формате: 'year-month-day'"
        text_for_user = self.replace_num(text_for_user)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_for_user)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите название сервера:',
                                 reply_markup=reply_markup)

        for num in range(-message_id, 1):
            try:
                message_id -= 3
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
            except Exception as ex:
                print(ex)
                break

        return self.COLLECTING_THE_TITLE

    def collecting_the_title(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Название сервера сохранено')
        update.message.reply_text('Введите IP сервера:', reply_markup=reply_markup)

        return self.COLLECTING_THE_IP

    def collecting_the_ip(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('IP сервера сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите логин от сервера:', reply_markup=reply_markup)

        return self.COLLECTING_THE_LOGIN

    def collecting_the_login(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Логин от сервера сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите пароль от сервера:', reply_markup=reply_markup)

        return self.COLLECTING_THE_PASSWORD

    def collecting_the_password(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Пароль от сервера сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите порт:', reply_markup=reply_markup)

        return self.COLLECTING_THE_PORT

    def collecting_the_port(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Порт сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите SSH:', reply_markup=reply_markup)

        return self.COLLECTING_THE_SSH

    def collecting_the_ssh(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('SSH сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите URL сервера:', reply_markup=reply_markup)

        return self.COLLECTING_THE_URL

    def collecting_the_url(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('URL сервера сохранен',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите дату начала периода оплаты:', reply_markup=reply_markup)

        return self.COLLECTING_THE_START_DATE

    def collecting_the_start_date(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Дата начала периода оплаты сохранена',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите дату конца периода оплаты:', reply_markup=reply_markup)

        return self.COLLECTING_THE_END_DATE

    def collecting_the_end_date(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Дата конца периода оплаты сохранена',
                                  reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Введите цену периода оплаты:', reply_markup=reply_markup)

        return self.COLLECTING_THE_PRICE

    def collecting_the_price(self, update, context):
        text = update.message.text

        if text == '-':
            text = None

        self.server_data.append(text)

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # sending a message and showing the keyboard
        update.message.reply_text('Цена периода оплаты сохранена',
                                  reply_markup=ReplyKeyboardRemove())

        data = self.server_data

        try:
            if data[-3] is not None and data[-2] is not None:
                data[-3] = self.fix_time(data[-3])
                data[-2] = self.fix_time(data[-2])

            data = data + [self.user_id]

            operator = Operator()

            operator.insert_into_server_table(data[:6] + [self.user_id])
            operator.insert_into_period_of_action(data[6:])

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Запись сохранена')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Для создания новой записи введите название сервера:",
                                 reply_markup=reply_markup)

        return self.RECORD_CREATING

    def help(self, update, context):
        pass

    def get_all_records(self, update, context):
        # getting the user id
        self.user_id = update.effective_user.id

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
        titles_ips = db_operator.get_all_titles_and_ips(self.user_id)
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}',
                                reply_markup=reply_markup)

        return self.TITLES_IP_STAGE

    def get_record_by_title(self, update, context):
        # getting the user id
        self.user_id = update.effective_user.id

        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        db_operator = Operator()
        titles_ips = db_operator.get_all_titles_and_ips(self.user_id)
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}')

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите название сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_TITLE

    def get_by_title_db(self, update, context):
        # getting the user id
        self.user_id = update.effective_user.id

        server_title = update.message.text

        try:
            operator = Operator()
            result = operator.get_by_title(server_title, self.user_id)
            result = self.fix_server_info(result)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Об этом сервере мне известно следующее:\n{result}')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите название сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_TITLE

    def get_record_by_ip(self, update, context):
        # getting the user id
        self.user_id = update.effective_user.id

        # Get CallbackQuery from Update
        query = update.callback_query
        query.answer()

        db_operator = Operator()
        titles_ips = db_operator.get_all_titles_and_ips(self.user_id)
        titles_ips = self.fix_titles_ips(titles_ips)

        query.edit_message_text(f'Названия и IP всех известных мне серверов:\n{titles_ips}')

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Введите IP сервера',
                                 reply_markup=reply_markup)

        return self.GETTING_BY_IP

    def get_by_ip_db(self, update, context):
        server_ip = update.message.text
        print(server_ip)

        try:
            operator = Operator()
            result = operator.get_by_ip(server_ip, self.user_id)
            result = self.fix_server_info(result)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Об этом сервере мне известно следующее:\n{result}')

        except Exception as ex:
            print(ex)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Что-то пошло не так.\nПопробуйте еще раз')

        keyboard = [
            [InlineKeyboardButton('Вернуться к началу', callback_data=str(self.RETURN_TO_START))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

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
                self.GETTING_BY_TITLE: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу$'), self.get_by_title_db)
                ],
                self.GETTING_BY_IP: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу$'), self.get_by_ip_db)
                ],
                self.RECORD_CREATING: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text & ~Filters.regex('^Вернуться к началу | Пример записи$'),
                                   self.collecting_the_title)
                ],
                self.COLLECTING_THE_TITLE: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_title)
                ],
                self.COLLECTING_THE_IP: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_ip)
                ],
                self.COLLECTING_THE_LOGIN: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_login)
                ],
                self.COLLECTING_THE_PASSWORD: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_password)
                ],
                self.COLLECTING_THE_PORT: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_port)
                ],
                self.COLLECTING_THE_SSH: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_ssh)
                ],
                self.COLLECTING_THE_URL: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_url)
                ],
                self.COLLECTING_THE_START_DATE: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_start_date)
                ],
                self.COLLECTING_THE_END_DATE: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_end_date)
                ],
                self.COLLECTING_THE_PRICE: [
                    CallbackQueryHandler(self.start_over, pattern='^' + str(self.RETURN_TO_START) + '$'),
                    MessageHandler(Filters.text, self.collecting_the_price)
                ],
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
