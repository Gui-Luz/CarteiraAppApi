import requests
from bs4 import BeautifulSoup


def check_if_symbol_is_valid(stock):
    valid_symbols = []
    url = 'https://console.hgbrasil.com/documentation/finance/symbols'
    r = requests.get(url)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.findAll('code', {'class':"highlighter-rouge"})
        for li in ul:
            valid_symbols.append(li.text)
        if stock.upper() in valid_symbols:
            return True
        else:
            return False
    else:
        return False