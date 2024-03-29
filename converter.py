import math
import json
import os

def convert_price(price_in_currency):

    # Округляем цену в большую сторону до целых единиц
    price_in_currency = math.ceil(price_in_currency)

    # Выбираем коэффициент для конвертации в рубли в зависимости от цены
    if price_in_currency < 100:
        coefficient = coefficients[f"less100{region}"]
    elif price_in_currency < 699:
        coefficient = coefficients[f"less699{region}"]
    elif price_in_currency < 1199:
        coefficient = coefficients[f"less1199{region}"]
    elif price_in_currency < 1799:
        coefficient = coefficients[f"less1799{region}"]
    else:
        coefficient = coefficients[f"more1799{region}"]


    if region == "tr" and coefficient != coefficients[f"less100{region}"]:
        # Прибавляем процент к цене
        price_in_currency += price_in_currency * coefficients[f"percent{region}"]
    elif region == "ua" and coefficient != coefficients[f"less300{region}"]:
        # Прибавляем процент к цене
        price_in_currency += price_in_currency * coefficients[f"percent{region}"]

    # Округляем цену в большую сторону до целых единиц или десятков в зависимости от региона
    if region == "ua":
        price_in_currency = math.ceil(price_in_currency / 10.0) * 10
    else:
        price_in_currency = math.ceil(price_in_currency)

    # Конвертируем цену в рубли
    price_in_rubles = price_in_currency * coefficient

    # Округляем цену в большую сторону до десятков
    price_in_rubles = math.ceil(price_in_rubles / 10.0) * 10

    return price_in_rubles



