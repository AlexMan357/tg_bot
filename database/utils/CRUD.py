from typing import Dict, List, TypeVar
from peewee import ModelSelect
from ..common.models import database_history, ModelBase
T = TypeVar('T')


def _store_data(database: database_history, model: T, *data: List[Dict]) -> None:
    """ Функция для добавления записей в базу данных"""
    with database_history.atomic():
        model.insert_many(*data).execute()


def _retrieve_all_data(database: database_history, model: T, *columns: ModelBase) -> ModelSelect:
    """ Функция - запрос для чтения всех записей из базы данных"""
    with database_history.atomic():
        response = model.select(*columns)
    return response


class CRUDInterface:
    """ Базовый класс для инкапсуляции функций модуля """
    @classmethod
    def create(cls):
        """ Функция возвращает ссылку на функцию добавления записей в базу данных"""
        return _store_data

    @classmethod
    def retrieve(cls):
        """ Функция возвращает ссылку на функцию чтения всех записей из базы данных"""
        return _retrieve_all_data


if __name__ == '__main__':
    _store_data()
    _retrieve_all_data()
    CRUDInterface()
