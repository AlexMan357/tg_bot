from peewee import ModelSelect
from site_API.core import site_api, host, url, headers, contacts
from TG_API.core import bot
from database.common.models import database_history, History
from database.core import crud
from datetime import datetime, timedelta
from typing import Dict
from telebot import types

page = 1

CONTENT_TYPES = ["text", "audio", "document", "photo", "stiker", "video", "video_note", "voice", "location",
                 "contact"]


@bot.message_handler(commands=['start', 'help'])
def get_start(message):
    """ Ф-я выводит информацию о работе бота """
    website_button_add(message=message)
    bot.send_message(message.chat.id, "Для получения информации о камне с сайта Столешка.Ру выполните"
                                      " одно из действий")

    bot.send_message(message.chat.id, "/req - получить новый запрос по скидкам\n"
                                      "/allbrands - показать все бренды\n"
                                      "/contacts - контакты\n"
                                      "/history - просмотреть историю запросов по скидкам\n"
                                      "/clearhistory - oчистить историю"
                     )


@bot.message_handler(commands=['history'])
def get_history(message):
    """ Ф-я выводит информацию из базы данных"""
    db_read = crud.retrieve()
    retrieved = db_read(database_history, History, History.date_field, History.title, History.price_current)

    today = datetime.now().date()
    history_days = (today, today - timedelta(days=1), today - timedelta(days=2))

    for element in retrieved:
        if element.date_field in history_days:
            bot.send_message(message.chat.id, ' '.join([str(element.date_field), str(element.title),
                                                        str(element.price_current)]))

    bot.send_message(message.chat.id, '/help')

@bot.message_handler(commands=['req', 'next'])
def get_request(message):
    """ Ф-я генерирует запрос к сайту и выводит результат """
    global page

    if message.text == '/req':
        page = 1

    new_params = '?PAGEN_1='
    response = response_generate(host=host, url=url, headers=headers, params=new_params + str(page))

    if response:
        bot.send_message(message.chat.id, "Запрос со страницы {page}".format(page=page))
        for element in response:
            bot.send_message(message.chat.id, ' '.join([str(element['title']), str(element['price_current']),
                                                        str(element['image'])]))

        date = datetime.now()
        sql = History.delete().where(History.date_field == date)
        sql.execute()

        db_write = crud.create()
        for element in response:
            db_write(database_history, History, element)

        if response_generate(host=host, url=url, headers=headers, params=new_params + str(page + 1)):
            page += 1
            bot.send_message(message.chat.id, 'Запрос к следующей странице: /next')
        else:
            stop_next(message)
            get_start(message)
    else:
        stop_next(message)


@bot.message_handler(commands=['contacts'])
def show_contacts(message):
    """ Ф-я генерирует запрос контактов """
    get_answer = site_api.get_contacts()
    response = get_answer(host=host, headers=headers, contacts=contacts)
    bot.send_message(message.chat.id, "Контакты: {response}".format(response=response))
    bot.send_message(message.chat.id, '/help')


@bot.message_handler(commands=['allbrands'])
def show_brands(message):
    """ Ф-я генерирует запрос брендов, представленных на сайте """
    get_answer = site_api.get_brands()
    response = get_answer(url=url, headers=headers)
    if response:
        for value in response:
            bot.send_message(message.chat.id, "{name}: {link}".format(name=value[0], link=host + value[1]))
    bot.send_message(message.chat.id, '/help')


@bot.message_handler(commands=['clearhistory'])
def clear_history(message):
    """ Ф-я очищает историю запросов """
    sql = History.delete()
    sql.execute()
    bot.send_message(message.chat.id, 'История запросов очищена.')
    bot.send_message(message.chat.id, '/help')


@bot.message_handler(content_types=CONTENT_TYPES)
def response_to_an_invalid_command(message):
    command_list = ['req', 'history', 'clearhistory', 'start', 'help', 'contacts', 'allbrands']
    if message.text not in command_list:
        get_start(message)


def stop_next(message):
    """" Ф- я для вывода ботом сообщения об отсутствии позиций"""
    bot.send_message(message.chat.id, "К сожалению, скидочных позиций больше нет")


def website_button_add(message):
    """ Ф-я выводит кнопку для ссылки на сайт """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Посетить сайт", url=host))
    bot.send_message(message.chat.id, 'Cсылка на сайт', reply_markup=markup)


def response_generate(host: str, url: str, headers: Dict[str, str], params: str) -> ModelSelect:
    """ Ф-я генерации запроса на сайт о скидках """
    get_answer = site_api.get_response()
    response = get_answer(host=host, url=url, headers=headers, params=params)
    return response


if __name__ == '__main__':
    get_history()
    get_request()
    website_button_add()
    response_generate()
