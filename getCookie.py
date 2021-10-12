import gzip
import json
import urllib
import selenium
import selenium.webdriver

baseUrl = "https://www.pyszne.pl/na-dowoz/jedzenie/"
# example: https://www.pyszne.pl/na-dowoz/jedzenie/bydgoszcz-bydgoszcz-85-021
URL = 'https://www.pyszne.pl/na-dowoz/jedzenie/bydgoszcz-bydgoszcz-85-021'
cookieLocation = 'savedCookie.json'

with open(cookieLocation) as json_file:
    cookieData = json.load(json_file)

# print((str(cookieData[0])[1:-1]).replace("'",'').replace(",",';'))

def urllibMethod(siteUrl, siteCookie):
    headers = siteCookie
    print(headers)

    request = urllib.request.Request(siteUrl, headers=headers)
    r = gzip.decompress(urllib.request.urlopen(request).read()) #It is implied that the webpage is gzipped, although a check might be necessary in future

    return(r)

urllibMethod('https://www.pyszne.pl/na-dowoz/jedzenie/gdansk-gdansk-80-728', cookieData)