import requests
import time
import csv
from bs4 import BeautifulSoup as bs



steam_headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
           'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Cookie': 'timezoneOffset=18000,0; steamMachineAuth76561198094698835=96631C3D12390760A2CBCF511F7F88B923729582; browserid=1064454454358045638; sessionid=47f066ec2cb72b37bc517c03; steamCountry=RU%7C00bd6acc9bb76cdf0bfc90824f710ea1; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1562788323%7D; app_impressions=730@2_100100_100101_100106; strInventoryLastContext=730_2; steamRememberLogin=76561198094698835%7C%7C3718b2ea45a43a69d024dfb8e699bdca; steamLoginSecure=76561198094698835%7C%7C91659CA142BEA5E30E553C38445C6D797060DFAC'
           }
steam_session = requests.Session()


def GetSteamPrice(url):
    request = steam_session.get(url, headers=steam_headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        prices = soup.find_all('span', attrs={'class': 'market_listing_price market_listing_price_with_fee'})
        is_price_get = False
        result = ''
        for price in prices:
            try:
                result = float(price.text[8:-10].replace(',', '.'))
                is_price_get = True
            except:
                pass
            if is_price_get:
                break
        #print('Цена в стим: ' + str(result))
        return result
    else:
        print('ERROR, status code: ' + str(request.status_code))
