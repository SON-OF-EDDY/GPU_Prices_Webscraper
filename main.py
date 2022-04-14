import time

from bs4 import BeautifulSoup
import requests
import re
import datetime

#CURRENT DATE AND TIME
current_date = datetime.datetime.now()
current_date = current_date.strftime("%A %B %Y, %H:%M:%S")

# FOR CONVERTING ALL USD VALUES INTO RUSSIAN RUBLES
usd_to_ruble_url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=RUB'
output = requests.get(url=usd_to_ruble_url).text
my_doc_2 = BeautifulSoup(output,'html.parser')
current_course = my_doc_2.find('p',class_="result__BigRate-sc-1bsijpp-1 iGrAod")
current_course_value = (current_course.text)
current_course_value_digits = (re.sub(pattern='[^0-9\.]+',string=current_course_value,repl=''))
current_course_value_digits = float(current_course_value_digits)


# EXTRACTING GPU USD PRICES FROM 'NEWEGG.COM'
gpu_list = ['RX 6600','RX 6700 XT','RTX 3050','RTX 3060','RTX 3060 Ti','RTX 3070','RTX 3070 Ti','RTX 3080',
            'RTX 3080 Ti','RX 6800 XT','RTX 3090','RX 6900 XT']

list_of_cheapest_prices = []

for gpu in gpu_list:

    list_of_prices = []

    url = f"https://www.newegg.com/p/pl?d={gpu}&Order=1&N=4131%204814"

    results = requests.get(url).text
    my_doc = BeautifulSoup(results,'html.parser')

    my_pattern = re.compile(pattern="^.*"+f"{gpu}"+".*$")

    price_tags = my_doc.find_all('div',class_='item-container')

    for entry in price_tags:
        text_child = entry.find('div',class_='item-info')
        grandchild = text_child.find('a',class_='item-title')
        valid_grandchild = re.search(pattern=my_pattern,string=grandchild.string)
        if valid_grandchild:
            current_price = entry.find('li',class_='price-current')
            try:
                refined = current_price.strong.text.replace(',','')
            except:
                refined = '0'
            if 500<int(refined)<1500:
                  list_of_prices.append(int(refined))

    if list_of_prices != []:
        cheapest_price = min(list_of_prices)
        russian_price = str(round(cheapest_price * current_course_value_digits))
        my_list = list(russian_price)
        max_length = len(my_list)
        needed_position = max_length - 3
        my_list.insert(needed_position,',')
        russian_price = ''.join(my_list)
        russian_price = f"₽{(russian_price)}"
        cheapest_price = f"${min(list_of_prices)}"
    else:
        cheapest_price = 'NOT FOUND!'
        russian_price = 'N/A'

    list_of_cheapest_prices.append([gpu,cheapest_price,russian_price])

print("POPULAR GPU's, CHEAPEST PRICES IN USD($) AND RUSSIAN RUBLES(₽):")
print("SOURCE:'NEWEGG.COM'")
print(f"CURRENT DATE: {current_date}")
print(f"CURRENT COURSE: $1 USD = ₽ {round(current_course_value_digits)} RUBLES")
print()
for entry in list_of_cheapest_prices:
    print(entry)






