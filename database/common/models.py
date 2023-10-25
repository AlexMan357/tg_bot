import peewee as pw
from datetime import datetime

database_history = pw.SqliteDatabase('history.db')


class ModelBase(pw.Model):
    """
    Класс базовой модели, который определяет базу данных
    Attributes:
            date_field (Date): поле для хранения даты-времени создания записи
    """
    date_field = pw.DateField(default=datetime.now())

    class Meta:
        """
        Класс для хранения конфигурации модели в пространстве имен
        Attributes:
            database (ModelBase): ссылка на базу данных
        """
        database = database_history


class History(ModelBase):
    """
    Класс модели базы данных, наследует подключение к базе данных
    Attributes:
        title (str): хранение наименованияя продукции
        image (Any): хранение ссылки на картинку с продукцией
        price_current (str): хранение текущей цены на продукцию
        price_current (str): хранение старой цены на продукцию
        size (str): хранение размера погонного метра продукции
    """
    title = pw.TextField()
    image = pw.AnyField()
    price_current = pw.TextField()
    price_old = pw.TextField()
    size = pw.TextField()
