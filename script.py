import math
import time
import random
import requests
from bs4 import BeautifulSoup

# Сколько максимально мест проверяем
max_pos = 180 

# По какому ключу ищем
key_target = "Мечники"

# Какое приложение ищем 
app_target = "com.elezthem.StickWar"


def make_request(page_num):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
    }
    params = {
    "query": "Мечники"
    }
    
    response = requests.get(url=f"""https://www.rustore.ru/catalog/search/page-{page_num}""", headers=headers, params=params)

    if response.status_code != 200:
        return None

    return response

def receive_aps_list(r):

    soup = BeautifulSoup(r.text, 'html.parser')

    app_links = soup.find_all('a', href=True)
    app_links = [a for a in app_links if '/catalog/app/' in a.get('href', '')]

    # Получаем список приложений на странице
    app_names = [a.get('href').replace("/catalog/app/", "") for a in app_links]

    return app_names



def search_target_app():

    n = math.ceil(max_pos / 36) # Сколько страниц нужно проверить
    code = 0
    pos = 0

    for i in range(n): 
        response = make_request(i+1)
        app_names = receive_aps_list(response)

        if app_names == None:
            code = 3
            break

        if app_names == []:
            code = 2
            break

        if app_target in app_names:
            code = 1
            pos = app_names.index(app_target) + 1 + (i*36)
            break

        time.sleep(random.randint(2,5)) # Случайная задержка между запросами




    if code == 0:
        return print(f"""Из {max_pos} приложений твоего нет""")
    elif code == 1:
        return print(f"""Мы его нашли. Место {pos}""")
    elif code == 2:
        return print(f"""Тебя собаку забанили на {i} странице""")
    elif code == 3:
        return print(f"Какая-то ошибка с запросом")

search_target_app()