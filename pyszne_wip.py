from bs4 import BeautifulSoup
from requests import get
import gzip
from collections import OrderedDict
from requests import Session
import socket
import cfscrape
import unicodedata
import re
import urllib

city = "gdansk"
postalCode = "80-728"
baseUrl = "https://www.pyszne.pl/na-dowoz/jedzenie/"
# example: https://www.pyszne.pl/na-dowoz/jedzenie/bydgoszcz-bydgoszcz-85-021

# Remove city name accents
def removeAccents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)

def parsePrice(price):
    return price.replace(' ','').replace('zł','').replace(',','.')

def pyszneplPost():

    return

# Get user localisation; City and postal code
def getUserLocalistaion():
    global city
    global postalCode
    city = removeAccents(input(f"City: ")).lower()
    postalCode = input(f"Polish postal code in '12-345' format: ")

    if re.match(r'[0-9][0-9]\-[0-9][0-9][0-9]', postalCode): 
        print("Correct postal code, continuing.")
        return True
    else:
        print("Bad postal code, exiting.")
        return False

def cfscrapeMethod(siteUrl):
    scraper = cfscrape.create_scraper()  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    return scraper.get(siteUrl).text  # => "<!DOCTYPE html><html><head>..."

def requestsMethod(siteUrl):
    s = Session()
    headers = OrderedDict({
        'Host': 'www.pyszne.pl',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=ld7fcj6ah62rs23fq4gmpols8l; realRefr=https%3A%2F%2Fwww.google.com%2F; s_2051430886=0; cookieConsent=temporary; searchstring=80-728%20Gda%C5%84sk; latitude=54.34973; longitude=18.67251; postcode=80-728; userExperiments=%7B%22id%22%3A%2299a30676-f774-42d8-bfaf-098820412cb8%22%2C%22attributes%22%3A%7B%7D%7D; localFavorites=[]; sortby=default; selectedFilters=%7B%22restoreFromCookie%22%3Afalse%7D; activeAddress=%7B%22address%22%3A%7B%22location%22%3A%7B%22city%22%3A%22Gda%C5%84sk%22%2C%22country%22%3A%22%22%2C%22deliveryAreaId%22%3A%2280-728%22%2C%22district%22%3A%22%22%2C%22lat%22%3A54.34973%2C%22lng%22%3A18.67251%2C%22locationSlug%22%3A%22gdansk-gdansk-80-728%22%2C%22placeId%22%3A%22%22%2C%22postalCode%22%3A%2280-728%22%2C%22state%22%3A%22Pomorskie%22%2C%22street%22%3A%22%22%2C%22streetNumber%22%3A%22%22%2C%22takeawayPostalCode%22%3A%2280-728%22%2C%22formattedAddress%22%3A%2280-728%20Gda%C5%84sk%22%2C%22id%22%3A%22%22%2C%22timeZone%22%3A%22%22%7D%2C%22shippingDetails%22%3A%7B%7D%2C%22savedAddressId%22%3A%22%22%7D%2C%22searchString%22%3A%2280-728%20Gda%C5%84sk%22%7D; __cf_bm=32Fcra679kSQ.xSTRjpOtEPT2gHNHsnhh62_bJgglbg-1634024840-0-AYP/NFwpBJM2uJ+qjCeGPbzqiXXYYIHyXGDyk0QvrHAktahPsF/H212dDMM6OQDkBDL0Le6arPcQMSRBKpvS5l9heXIDHGFRo6R1qtmmtEzP',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    })
    response = get(siteUrl, headers=headers)
    return(response)

def urllibMethod(siteUrl):
    headers = {
        'Host': 'www.pyszne.pl',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=ld7fcj6ah62rs23fq4gmpols8l; realRefr=https%3A%2F%2Fwww.google.com%2F; s_2051430886=0; cookieConsent=temporary; searchstring=80-728%20Gda%C5%84sk; latitude=54.34973; longitude=18.67251; postcode=80-728; userExperiments=%7B%22id%22%3A%2299a30676-f774-42d8-bfaf-098820412cb8%22%2C%22attributes%22%3A%7B%7D%7D; localFavorites=[]; sortby=default; selectedFilters=%7B%22restoreFromCookie%22%3Afalse%7D; activeAddress=%7B%22address%22%3A%7B%22location%22%3A%7B%22city%22%3A%22Gda%C5%84sk%22%2C%22country%22%3A%22%22%2C%22deliveryAreaId%22%3A%2280-728%22%2C%22district%22%3A%22%22%2C%22lat%22%3A54.34973%2C%22lng%22%3A18.67251%2C%22locationSlug%22%3A%22gdansk-gdansk-80-728%22%2C%22placeId%22%3A%22%22%2C%22postalCode%22%3A%2280-728%22%2C%22state%22%3A%22Pomorskie%22%2C%22street%22%3A%22%22%2C%22streetNumber%22%3A%22%22%2C%22takeawayPostalCode%22%3A%2280-728%22%2C%22formattedAddress%22%3A%2280-728%20Gda%C5%84sk%22%2C%22id%22%3A%22%22%2C%22timeZone%22%3A%22%22%7D%2C%22shippingDetails%22%3A%7B%7D%2C%22savedAddressId%22%3A%22%22%7D%2C%22searchString%22%3A%2280-728%20Gda%C5%84sk%22%7D; __cf_bm=ZjviCOdK7IoBhYkawG6BVu.QmTwvcNjbxXf0M8pT2qk-1634026665-0-AQxgwoDwpBT+K0UKLn5g1zJDAkJ8UIYGx87MvmZYyMHX/rN76NVW7MR/dnBvU2TcE60hlOZ41kLaraABMIhAyunwQKQKnd4LvcrdO/5vf1hX',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
        }
    request = urllib.request.Request(siteUrl, headers=headers)
    r = gzip.decompress(urllib.request.urlopen(request).read())

    return(r)


def main():
    # if not(getUserLocalistaion()): return
    print(city,postalCode)
    URL = baseUrl + city + '-' + city + '-' + postalCode
    print(URL)
    page = urllibMethod(URL)
    bs = BeautifulSoup(page, features='html.parser')
    for offer in bs.find_all('ul', 'aria-label', "Otwarte"):
        # dostawa = offer.find('p', class_='price').get_text().strip()
        offerTitle = offer.find('a', 'title').get_text().strip()
        # print(f'{offerTitle}\n {parse_price(koszt)}')
        print(f'{offerTitle}')


if __name__ == "__main__":
    main()