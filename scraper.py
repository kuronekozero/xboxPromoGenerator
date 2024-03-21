from bs4 import BeautifulSoup
import requests
from converter import convert_price

def parse_game_info(game_link):
    # Отправляем запрос на сервер и получаем HTML-код страницы
    response = requests.get(game_link)
    html = response.text

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем элемент с названием игры
    game_title_element = soup.find('div', {'class': 'game-title-info-name'})
    game_title = game_title_element.text

    # Ищем div с классом "game-title-info"
    game_info_div = soup.find('div', {'class': 'game-title-info'})

    # Ищем все теги <a> с атрибутом itemprop="item" и извлекаем текст из вложенных тегов <span>
    platform_elements = game_info_div.find_all('a', {'itemprop': 'item'})
    platforms = [platform.find('span', {'itemprop': 'name'}).text.replace(' ', '') for platform in platform_elements]

    # Ищем тег <meta> с атрибутом itemprop="price" и извлекаем значение его атрибута content
    price_element = soup.find('meta', {'itemprop': 'price'})
    price_in_peso = float(price_element['content']) if price_element else 0

    # Определяем регион игры
    if "ua-store" in game_link:
        region = "ua"
    elif "tr-store" in game_link:
        region = "tr"

    # Конвертируем цену в рубли
    # price_in_rubles = convert_price(price_in_lira, region)

    # Добавляем символ рубля к цене
    #price = f"{price_in_rubles}₽"

    month_dict_tr = {
        "Oca": "Января",
        "Şub": "Февраля",
        "Mar": "Марта",
        "Nīs": "Апреля",
        "May": "Мая",
        "Haz": "Июня",
        "Tem": "Июля",
        "Ağu": "Августа",
        "Eyl": "Сентября",
        "Eki": "Октября",
        "Kas": "Ноября",
        "Ara": "Декабря"
    }

    month_dict_ua = {
        "січе.": "Января",
        "люти.": "Февраля",
        "бере.": "Марта",
        "квіт.": "Апреля",
        "трав.": "Мая",
        "черв.": "Июня",
        "липе.": "Июля",
        "серп.": "Августа",
        "вере.": "Сентября",
        "жовт.": "Октября",
        "лист.": "Ноября",
        "груд.": "Декабря"
    }

    # Ищем тег <span> с классом "game-cover-save-bonus" и извлекаем его текст
    discount_bonus_element = soup.find('span', {'class': 'game-cover-save-bonus'})
    discount_regular_element = soup.find('span', {'class': 'game-cover-save-regular'})

    # Ищем тег <p> с классом "game-cover-bottom-small" и извлекаем его текст
    discount_end_date_element = soup.find('p', {'class': 'game-cover-bottom-small'})
    if discount_end_date_element:
        discount_end_date = discount_end_date_element.text
        if "ua-store" in game_link:
            discount_end_date = discount_end_date.replace("Закінчується:", "Скидка действует до:")
            # Заменяем украинские сокращения на русские названия месяцев
            for ukrainian, russian in month_dict_ua.items():
                discount_end_date = discount_end_date.replace(ukrainian, russian)
        elif "tr-store" in game_link:
            discount_end_date = discount_end_date.replace("Ends:", "Скидка действует до:")
            # Заменяем турецкие сокращения на русские названия месяцев
            for turkish, russian in month_dict_tr.items():
                discount_end_date = discount_end_date.replace(turkish, russian)
        # Удаляем "р." из даты
        discount_end_date = discount_end_date.replace(" р.", "")
    else:
        discount_end_date = ''

    if discount_bonus_element:
        discount = discount_bonus_element.text
    elif discount_regular_element:
        discount = discount_regular_element.text
    else:
        discount = ''

    # Ищем все теги <li> с атрибутом itemprop="itemListElement"
    list_elements = soup.find_all('li', {'itemprop': 'itemListElement'})

    # Извлекаем текст из вложенного тега <span> с атрибутом itemprop="name" для тега <li>, у которого <meta itemprop="position" content="3">
    platforms = ''
    for list_element in list_elements:
        meta_tag = list_element.find('meta', {'itemprop': 'position', 'content': '3'})
        if meta_tag:
            platforms = list_element.find('span', {'itemprop': 'name'}).text.replace(' ', '')
            break

    if platforms == "XboxSeriesX|S":
        platforms = "Xbox Series X|S"
    elif platforms == "XboxOne":
        platforms = "ONE&Series X|S"

    # Ищем ссылку на страницу игры в PS Store
    ps_store_link_element = soup.find('a', {'class': 'game-buy-button-href'})
    ps_store_link = ps_store_link_element['href'] if ps_store_link_element else ''

    # Отправляем запрос на сервер и получаем HTML-код страницы PS Store
    response = requests.get(ps_store_link)
    html = response.text

    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Ищем теги <dd> с атрибутами data-qa для PS4 и PS5
    voice_values = []
    for attr in ["gameInfo#releaseInformation#voice-value", "gameInfo#releaseInformation#ps4Voice-value", "gameInfo#releaseInformation#ps5Voice-value"]:
        element = soup.find('dd', {'data-qa': attr})
        if element:
            voice_values.append(element.text)

    subtitles_values = []
    for attr in ["gameInfo#releaseInformation#subtitles-value", "gameInfo#releaseInformation#ps4Subtitles-value", "gameInfo#releaseInformation#ps5Subtitles-value"]:
        element = soup.find('dd', {'data-qa': attr})
        if element:
            subtitles_values.append(element.text)

    # Проверяем, содержат ли тексты "Rusça" или "російська"
    if any("Rusça" in value or "російська" in value for value in voice_values):
        language = "ПОЛНОСТЬЮ НА РУССКОМ"
    elif any("Rusça" in value or "російська" in value for value in subtitles_values):
        language = "РУССКИЕ СУБТИТРЫ"
    elif voice_values or subtitles_values:  # Если были найдены теги с информацией о языке
        language = "АНГЛИЙСКИЙ ЯЗЫК"
    else:
        language = ""  # Если теги с информацией о языке не были найдены

    if discount != "":
        discount = "-" + str(discount)

    return game_title, platforms, price_in_peso, discount, language, discount_end_date
