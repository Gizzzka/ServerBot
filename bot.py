from db import Operator
from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters, MessageFilter
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from datetime import date
import logging
import pprint


TOKEN = '1702573887:AAG3qF6cjRWbgs6gfOqRLI1sXwWg5P5vuh0'

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class FilterNewNote(MessageFilter):
    def filter(self, message):
        return 'Новая запись' in message.text


class FilterAllNotes(MessageFilter):
    def filter(self, message):
        return 'Получить все записи' in message.text


class FilterNoteByTitle(MessageFilter):
    def filter(self, message):
        return 'Получить запись по названию' in message.text


class FilterNoteByIp(MessageFilter):
    def filter(self, message):
        return 'Получить запись по ip' in message.text


def fix_info(info):
    final = ''

    for key, value in info.items():
        final += f'{key}: {value}\n'
        print(final)

    return final[:-1]


def start(update, context):
    custom_keyboard = [['Новая запись'],
                       ['Получить все записи'],
                       ['Получить запись по названию'],
                       ['Получить запись по ip']]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Выберете команду из списка',
                             reply_markup=reply_markup)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def new_note(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Эта функция, к великому сожалению, еще не реализована!')


new_note_filter = FilterNewNote()
new_note_handler = MessageHandler(new_note_filter, new_note)
dispatcher.add_handler(new_note_handler)


def get_all_notes(update, context):
    operator = Operator()

    result = operator.get_all_info()
    result = fix_info(result)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=result)


all_notes_filter = FilterAllNotes()
all_notes_handler = MessageHandler(all_notes_filter, get_all_notes)
dispatcher.add_handler(all_notes_handler)


def get_note_by_title(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Эта функция, к великому сожалению, еще не реализована!')


get_note_by_title_filter = FilterNoteByTitle()
get_note_by_title_handler = MessageHandler(get_note_by_title_filter, get_note_by_title)
dispatcher.add_handler(get_note_by_title_handler)


def get_note_by_ip(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Эта функция, к великому сожалению, еще не реализована!')


get_note_by_ip_filter = FilterNoteByIp()
get_note_by_ip_handler = MessageHandler(get_note_by_ip_filter, get_note_by_title)
dispatcher.add_handler(get_note_by_ip_handler)


updater.start_polling()
