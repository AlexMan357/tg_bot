from site_API.util.site_api_handler import SiteApiInterface

host = 'https://www.stoleshka.ru'
url = 'https://www.stoleshka.ru/catalog/akrilovyy_kamen/'

headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

params = '?PAGEN_1=1'
contacts = '/about/contacts/'

site_api = SiteApiInterface()

# if __name__ == '__main__':
#     site_api()
