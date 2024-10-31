import requests
from bs4 import BeautifulSoup
import json


def get_all_of_page(url: str):
    # Список для хранения всех цитат
    quotes_list_of_page = []
    # Получаем страницу
    response = requests.get(url)
    if response.status_code == 200:
        # Парсим содержимое страницы
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ищем все цитаты
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            # Извлекаем текст цитаты
            text = quote.find('span', class_='text').get_text()
            # Извлекаем автора цитаты
            author = quote.find('small', class_='author').get_text()
            # Извлекаем теги
            tags = quote.find('div', class_='tags').find_all('a', class_='tag')
            tags_list = [tag.get_text() for tag in tags]
            # Добавляем информацию о цитате в список
            quotes_list_of_page.append({
                'text': text,
                'author': author,
                'tags': tags_list
            })
    return quotes_list_of_page


# URL целевой страницы
url = 'https://quotes.toscrape.com/'
result_list_all_page: list = []
for i in range(1, 11):
    result = get_all_of_page(url=url+f"/page/{i}")
    result_list_all_page.append({f"page_{i}": result})

    # Упаковываем список всех цитат в JSON
with open('quotes.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_list_all_page, json_file, ensure_ascii=False, indent=4)
    print(f'Successfully saved {len(result_list_all_page)} quotes to quotes.json')
