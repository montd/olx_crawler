from bs4 import BeautifulSoup
import json
import gzip
import unicodedata
import re
import os
import urllib
import urllib.request 
import selenium
import selenium.webdriver

#for testing purposes
userCity = "gdansk"
userPostalCode = "80-728"
baseUrl = "https://www.pyszne.pl/na-dowoz/jedzenie/"
# example: https://www.pyszne.pl/na-dowoz/jedzenie/bydgoszcz-bydgoszcz-85-021
siteCookie = ''
cookieLocation = 'savedCookie.json'


class siteHandling():
    
    def getCookie(siteUrl): # Get fresh cookies from combined url if needed
        """Expecting siteURL for the selenium GET function"""
        driver = selenium.webdriver.Firefox()
        driver.get(siteUrl)
        cookiesDataRaw = driver.get_cookies()
        cookiesData = "set-cookie:" + (str(cookiesDataRaw[0])[1:-1]).replace('"name":','').replace('"value":','').replace("'",'').replace(",",';').replace(":",' =')
        print(cookiesData)
        with open(cookieLocation, 'w') as outfile:
            json.dump(cookiesData, outfile)
        with open('rawcookie.json', 'w') as outfile:
            json.dump(cookiesDataRaw, outfile, indent=3)
        driver.close()
        return cookiesData
  
    def loadCookie(cookieLocation): # Load saved cookie or get a first one
        try:
            if os.stat(cookieLocation).st_size > 0:
                with open(cookieLocation) as json_file:
                    return json.load(json_file)
        except OSError:
            print('There is no cookie file yet...')
        return False
        
    def urllibMethod(siteUrl, siteCookie):
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
            'Cookie': str(siteCookie),
            'Cache-Control': 'max-age=0',
            'TE': 'trailers',
            }
        request = urllib.request.Request(siteUrl, headers=headers)
        r = gzip.decompress(urllib.request.urlopen(request).read()) #It is implied that the webpage is gzipped, although a check might be necessary in future

        return(r)


class userInput():
    # Get user localisation; City and postal code
    def getUserLocalistaion():
        userCity = userInput.removeAccents(input(f"City: ")).lower()
        userPostalCode = input(f"Polish postal code in '12-345' format: ")
        if re.match(r'[0-9][0-9]\-[0-9][0-9][0-9]', userPostalCode): 
            print("Correct postal code, continuing.")
            return userCity,userPostalCode
        else:
            print("Bad postal code, exiting.")
            return False
    # Remove city name accents
    def removeAccents(text):
        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")
        return str(text)

class pageGetProcessing():
    def parsePrice(price):
        return price.replace(' ','').replace('zł','').replace(',','.')


def main():
    # if not(getUserLocalistaion()): return
    print(userCity,userPostalCode)
    URL = baseUrl + userCity + '-' + userCity + '-' + userPostalCode
    print(URL)
    siteCookie = siteHandling.loadCookie(cookieLocation)
    print('Site cookie type: ', type(siteCookie))
    page = ''
    if siteCookie != False: 
        for i in range(0,1):
            try: 
                page = (siteHandling.urllibMethod(URL,siteCookie))
                print(page[:100])
                break
            except urllib.error.HTTPError:
                print("Cookies probably expired, will try to get new ones.")
                siteCookie = siteHandling.getCookie(URL)
            print("Failed to make cookies work :(")
        return
    else:
        siteCookie = siteHandling.getCookie(URL)
    print(page[:100])

    bs = BeautifulSoup(page, features='html.parser')
    for offer in bs.find_all('ul'):
        # dostawa = offer.find('p', class_='price').get_text().strip()
        offerTitle = offer.find('a', 'title').get_text().strip()
        # print(f'{offerTitle}\n {parse_price(koszt)}')
        print(f'{offerTitle}')


if __name__ == "__main__":
    main()