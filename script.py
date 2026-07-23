import requests
import math
from bs4 import BeautifulSoup

# Сколько максимально мест проверяем
max_pos = 180 

# По какому ключу ищем
key_target = "Мечники"

# Какое приложение ищем 
app_target = "com.DEVll.ninjagaiden2thedarkswordofchaos"


def make_request(page_num):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
}
    params = {
    "query": "Мечники"
}

    return requests.get(url=f"""https://www.rustore.ru/catalog/search/page-{page_num}""", headers=headers, params=params)

def receive_aps_list(r):

    soup = BeautifulSoup(r.text, 'html.parser')

    app_links = soup.find_all('a', href=True)
    app_links = [a for a in app_links if '/catalog/app/' in a.get('href', '')]

    # Получаем список приложений на странице
    app_names = [a.get('href').replace("/catalog/app/", "") for a in app_links]

    return app_names



def search_target_app():

    n = math.ceil(max_pos / 36) # Сколько страниц нужно проверить
    flag = False
    pos = 0

    for i in range(n): 
        response = make_request(i+1)
        app_names = receive_aps_list(response)

        if app_target in app_names:
            flag = True
            pos = app_names.index(app_target) + 1 + (n*36)
            break

    if flag:
        return print(f"""Мы его нашли. Место {pos}""")
    else:
        return print(f"""Из {max_pos} приложений твоего нет""")

search_target_app()