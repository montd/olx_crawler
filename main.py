from bs4 import BeautifulSoup
from requests import get

def parse_price(price):
    return price.replace(' ','').replace('zł','').replace(',','.')



def main():
    URL = "https://www.olx.pl/nieruchomosci/gdansk/?search%5Bfilter_float_price%3Afrom%5D=400&search%5Bfilter_float_price%3Ato%5D=1200&search%5Bprivate_business%5D=private&search%5Bdistrict_id%5D=135&reason=observed_search"
    page = get(URL)
    bs = BeautifulSoup(page.content, features='html.parser')

    for offer in bs.find_all('div', class_="offer-wrapper"):
        koszt = offer.find('p', class_='price').get_text().strip()
        offerTitle = offer.find('strong').get_text().strip()
        link = offer.find('a')
        print(link['href'])
        print(f'{offerTitle}\n {parse_price(koszt)}')


if __name__ == "__main__":
    main()