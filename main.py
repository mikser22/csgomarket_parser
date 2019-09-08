import requests
import time
import csv
from bs4 import BeautifulSoup as bs
import steam_price_check as steam


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
           'Accept-Encoding': 'gzip, deflate, br',
           'Connection': 'keep-alive',
           'Cookie': '__cfduid=d8b75804a56a288ee377dc0e623c766081562748266; cf_clearance=2f76885d59e74bcf2000b4a817bfdfeb42b480ce-1567940908-2700-150'
           }

PAGE_COUNT = 800
base_url = 'https://market.csgo.com'
file_name = 'parse_guns.csv'

with open(file_name, 'w') as file:
    a_pen = csv.writer(file)
    a_pen.writerow(('URL', 'Текущая цена', 'Цена стим', 'Выгода'))
file.close()
session = requests.Session()
quality_dict = {'После полевых испытаний': 'Field-Tested', 'Прямо с завода': 'Factory New',
                'Немного поношенное': 'Minimal Wear', 'Закаленное в боях': 'Battle-Scarred', 'Поношенное': 'Well-Worn'}

fail_count = [0, 0]


def FindPrice(page):
    request = session.get(page, headers=headers)
    if request.status_code == 200:
        try:
            soup = bs(request.content, 'html.parser')
            current_price_tmp = soup.find_all('div', attrs={'class': 'ip-bestprice'})
            current_price = float(current_price_tmp[0].text)
            steam_url = GetItemName(page)
            steam_price = steam.GetSteamPrice(steam_url)
            fail_count[1] += 1
            if steam_price == '':
                fail_count[0] += 1
            print('Ошибок цены стим: {}, всего рассмотрено: {}'.format(fail_count[0], fail_count[1]))
            if current_price < steam_price:
                FileWriter(page, current_price, steam_price)
                print('Текущая цена: {}\nЦена в Стим: {}'.format(current_price, steam_price))
                print(page)
                print('Выгода {} руб\n\n'.format(steam_price - current_price))
        except:
            pass
    else:
        print('Ошибка взятия цены')


def FindItemsOnPage(soup):
    div = soup.find_all('div', attrs={'id': 'applications', 'class': 'market-items'})
    hrefs = div[0].find_all('a')
    urls = []
    for a in hrefs:
        new_url = base_url + a['href']
        urls.append(new_url)
    return urls


def FindAllPages():
    page_list = []
    a = 1
    while a < PAGE_COUNT:
        page_url = 'https://market.csgo.com/?p={}'.format(a)
        page_list.append(page_url)
        a += 1
    return page_list


def FileWriter(url, cur_price, steam_price):
    with open(file_name, 'a') as file:
        a_pen = csv.writer(file)
        #a_pen.writerow((url, cur_price, mid_price, round(mid_price - cur_price, 2)))
        a_pen.writerow((url, cur_price, steam_price, round(steam_price - cur_price, 2)))
    file.close()


def Start():
    page_list = FindAllPages()
    count = 0
    for page in page_list:
        request = session.get(page, headers=headers)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser')
            urls = FindItemsOnPage(soup)
            for item in urls:
                FindPrice(item)
                time.sleep(2)
        else:
            time.sleep(30)
            print('ERROR, status code: ' + str(request.status_code))
        print('Страница {} просмотрена'.format(count))
        count += 1
        time.sleep(0.2)


def GetItemName(page):
    request = session.get(page, headers=headers)
    steam_url = 'https://steamcommunity.com/market/listings/730/'
    if request.status_code == 200:
        try:
            soup = bs(request.content, 'html.parser')
            div = soup.find_all('div', attrs={'class': 'item-stat'})
            name = div[2].find('h3').text[:-17]
            link = soup.find('link', attrs={'rel': 'canonical'})['href']
            pos = link.find('| ')
            tmp = link[pos + 1:]
            main_pos = name.find('| ')
            text = name[:main_pos+1] + tmp
            return steam_url + text
        except:
            pass
    else:
        print('Ошибка')


Start()