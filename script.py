import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_search_results(query):
    """
    Выполняет поиск на RuStore и возвращает список package_name в порядке выдачи
    """
    url = f"https://www.rustore.ru/catalog/search?query={query}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Ошибка: статус-код {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим все ссылки на приложения
    app_links = soup.find_all('a', href=True)
    app_links = [a for a in app_links if '/catalog/app/' in a.get('href', '')]
    
    # Извлекаем package_name
    package_names = []
    for link in app_links:
        href = link.get('href')
        package_name = href.replace('/catalog/app/', '')
        package_names.append(package_name)
    
    return package_names


def find_app_position(package_names, target_package):
    """
    Ищет позицию приложения в списке
    Возвращает позицию (начиная с 1) или None, если не найдено
    """
    if target_package in package_names:
        return package_names.index(target_package) + 1
    return None


# -------- Основная часть скрипта --------

# Ввод данных от пользователя
target_package = input("Введите package_name игры друга: ")
keywords_input = input("Введите ключевые слова через запятую: ")
keywords = [kw.strip() for kw in keywords_input.split(',')]

print("\n" + "="*60)
print("Результаты поиска:")
print("="*60)

for keyword in keywords:
    print(f"\n🔍 Поиск по запросу: '{keyword}'")
    
    # Получаем результаты поиска
    results = get_search_results(keyword)
    
    if not results:
        print("  ❌ Не удалось получить результаты")
        continue
    
    print(f"  📊 Найдено приложений: {len(results)}")
    
    # Ищем позицию
    position = find_app_position(results, target_package)
    
    if position:
        print(f"  ✅ Игра найдена на позиции {position}!")
        # Показываем соседей для контекста
        start = max(0, position - 3)
        end = min(len(results), position + 3)
        print(f"  📋 Соседние приложения:")
        for i in range(start, end):
            marker = "👉 " if i == position - 1 else "   "
            print(f"    {marker} {i+1}. {results[i]}")
    else:
        print(f"  ❌ Игра не найдена в первых {len(results)} результатах")

print("\n" + "="*60)
print("✅ Готово!")