import math
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

import bd_requests 

# Сколько максимально мест проверяем
max_pos = 180 

# По каким ключам мы ищем
keys = [
    "Мечники",
    "Стрелялки",
    "Пол это лава"
]

# Какое приложение ищем 
app_target = "com.autoverse.floorislava"

bd = bd_requests.DATABASE()

def make_request(page_num, key):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
    }
    params = {
        "query": key
    }
    
    response = requests.get(url=f"""https://www.rustore.ru/catalog/search/page-{page_num}""", headers=headers, params=params, timeout=10)

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



def search_target_app(keys):

    n = math.ceil(max_pos / 36) # Сколько страниц нужно проверить

    for key in keys:

        code = 0
        pos = 0

        for i in range(1, n+1): 
            response = make_request(i, key)
            app_names = receive_aps_list(response)

            if app_names == None:
                code = 3
                break

            if app_names == []:
                code = 2
                break

            if app_target in app_names:
                code = 1
                pos = app_names.index(app_target) + 1 + (i-1)*36
                break

            time.sleep(random.randint(10,17)) # Случайная задержка между запросами

        if code == 0:
            print(f"""Из {max_pos} приложений твоего по ключу -{key}- нет, лошок""")
        elif code == 1:
            print(f"""По ключу -{key}- место {pos}, страница {i}""")
            bd.open()
            bd.add_key_pos(app_target, key, pos, datetime.now().date())
        elif code == 2:
            print(f"""Тебя собаку забанили на ключе -{key}- {i} странице""")
        elif code == 3:
            print(f"Какая-то ошибка с запросом на ключе {key}")



search_target_app(keys)