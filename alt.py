from selenium import webdriver
from selenium.webdriver.common.keys import Keys
PATH = "D:\Pr0\Python\Scraper\chromedriver.exe"
driver = webdriver.Chrome(PATH)

def main():
    driver.get("https://pyszne.pl")
    assert "Pyszne.pl" in driver.title
    print(len(driver.find_element_by_id('imysearchstring')))
    driver.find_element_by_id('imysearchstring').send_keys('Siennicka 52/3')


    driver.find_element_by_id('submit_deliveryarea')
#id="imysearchstring"
#id="submit_deliveryarea"
    return


if __name__ == "__main__":
    main()