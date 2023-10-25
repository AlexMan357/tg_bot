import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple


def _make_response(host: str, url: str, headers: Dict[str, str], params: str, success: int = 200) -> List[Dict]:
    """ Ф-я собирает данные о скидках с сайта, возвращает данные в виде списка словарей """

    url = url + params
    page = requests.get(url, headers=headers, params=params)
    if page.status_code == success:
        soup = BeautifulSoup(page.text.encode('utf8'), "html.parser")
        items = soup.findAll('div', class_='product-item')
        stones = []

        for item in items:
            stones.append(
                {
                    "title": item.find('div', class_='product-item-title').get_text(strip=True),
                    "image": host + item.find('a', class_='product-item-image-wrapper').get('href'),
                    "price_current": item.find('div', class_='product-item-info-container product-item-price-container').
                    find('span', class_='product-item-price-current').get_text(strip=True),
                    "price_old": item.find('div', class_='product-item-info-container product-item-price-container').
                    find('span', class_='product-item-price-old').get_text(strip=True),
                    "size": ' '.join([item.find('input', class_="product-item-amount-field").get('value'),
                                      item.find('span', class_="product-item-amount-description-container").get_text(
                                          strip=True)])

                }
            )
        response = []
        for element in stones:
            if (float(element['price_old'][:-5].replace(' ', '')) -
                float(element['price_current'][:-5].replace(' ', ''))) * \
                 100 / float(element['price_old'][:-5].replace(' ', '')) >= 50:
                response.append(element)

        return response


def _get_contacts(host: str, headers: Dict[str, str], contacts: str, success: int = 200) -> str:
    """ Ф-я собирает данные контактов  с сайта """
    url = host + contacts
    page = requests.get(url, headers=headers)
    if page.status_code == success:
        soup = BeautifulSoup(page.text.encode('utf8'), 'html.parser')
        items = soup.findAll('p')

        response = []
        for item in items:
            result = item.text.replace('/xa0', '').strip()
            if result:
                response.append(result)
        return ' '.join(response)


def _get_brands(url: str, headers: Dict[str, str], success: int = 200) -> List[Tuple]:
    """ Ф-я собирает данные о брендах на сайте """
    page = requests.get(url, headers=headers)
    if page.status_code == success:
        soup = BeautifulSoup(page.text.encode('utf8'), 'html.parser')
        items = soup.findAll('h2', class_='bx_catalog_tile_title')
        response = []
        for item in items:
            result = item.find('a').get('href')
            if result:
                response.append((item.text.strip(), result))
        return response


class SiteApiInterface:
    """ Базовый класс для инкапсуляции функций модуля """
    @classmethod
    def get_response(cls):
        """ Ф-я возвращает ссылку на функцию, выполняющую парсинг сайта"""
        return _make_response

    @classmethod
    def get_contacts(cls):
        """ Ф-я возвращает ссылку на функцию, выполняющую сбор данных о контактах"""
        return _get_contacts

    @classmethod
    def get_brands(cls):
        """ Ф-я возвращает ссылку на функцию, выполняющую сбор данных о брендах, представленных на сайте"""
        return _get_brands


if __name__ == '__main__':
    _make_response()
    SiteApiInterface()
