import json
import time

from typing import List, Dict, Tuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

# Set up Chrome options and driver
options: webdriver.ChromeOptions = webdriver.ChromeOptions()
binary_yandex_driver_file: str = 'yandexdriver.exe'
driver: webdriver.Chrome = webdriver.Chrome(f"D:/Downloads/{binary_yandex_driver_file}", options=options)

# Navigate to Yandex website
driver.get("https://yandex.ru/")

# Set up cookies for the website
cookies: Dict[str, str] = {
    '_mygtm_utm_yclid': 'undefined',
    '_mygtm_utm_fbclid': 'undefined',
    'BITRIX_SM_COOKIE_ACCEPTION': 'true',
    'clientid': '1657034149548.6593574739',
    '_mygtm_utm_wbraid': 'undefined',
    'tmr_reqNum': '82',
    '_ym_isad': '2',
    '_ym_uid': '1657034150783971670',
    '_ym_d': '1657034150',
    '_gcl_au': '1.1.419134432.1657034150',
    '_mygtm_gpb_own_cookie': '1657034149548.6593574739',
    '_mygtm_utm_pb_clickid': 'undefined',
    '_mygtm_utm_gbraid': 'undefined',
    'tmr_lvidTS': '1657034149875',
    'tmr_lvid': '5a784389a8b58039ed7d55452f9b871d',
    '_mygtm_utm_gclid': 'undefined',
    '_mygtm_utm_ymclid': 'undefined',
    '_ym_visorc': 'b',
    'ab_version': 'original',
    'BITRIX_SM_CITY_REAL_ID': '693',
    'BITRIX_SM_USER_CITY': '%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80',
    'consumer_credit_calculator': '{"sumIn":5000000,"term":84}',
    'flocktory-uuid': '9b520c78-de3b-41db-901e-2b13f7540947-2',
    'ga_all_param': '',
    'PHPSESSID': 'fnyDoAORp2R1YX1QdlALNFccPJD2rnQd',
    'st_uid': '24a2781933998c5c916e6f06c5b03e77',
    'tmr_detect': '0|1657093858364'
}

# Add cookies to the driver
for name, value in cookies.items():
   driver.add_cookie({'name': name, 'value': value})

# Navigate to Yandex Maps and get the HTML of the page
driver.get(
    "https://yandex.ru/maps/?display-text=Сбербанк%20России%2C%20отделения&ll=144.462854%2C40.904234&mode=search&sctx=ZAAAAAgBEAAaKAoSCYnQCDauz0JAEabtX1lp4EtAEhIJA137Anqh8j8RmPxP%2Fu4d7D8iBgABAgMEBSgAOABAkE5IAWIXc291cmNlPWJ1c2luZXNzOmV4cF9yZWZqAnJ1nQHNzEw9oAEAqAEAvQHLe6nKwgF957enhAT7kbilBsSImpwE4fqP8AOgseyMBP6c2q8EjIz1mwSNiqeQBLXOjocE7JOL4gOcuI3nBI7fgIcE3rLc5APxufjcA6btn%2B4D8fajnQXbqZOcBMOPx%2FIDx%2BOBnATkvZGaBJ3v7e0DvJyjogThxciNBPry%2FowExPvN3wPqAQDyAQD4AQCCAhJjaGFpbl9pZDooNjAwMzYxMimKAgCSAgCaAgxkZXNrdG9wLW1hcHM%3D&sll=144.462854%2C40.904234&sspn=369.843750%2C137.610782&text=chain_id%3A%286003612%29&z=2")


def get_main_page(driver: WebDriver) -> str:
    '''Scrolls down the main page and saves the HTML to a file called "sber.html" in UTF-8 encoding.

    Args:
        driver: The WebDriver instance.

    Returns:
        The HTML of the main page.
    '''
    for i in range(500):
        element = driver.find_elements(By.CLASS_NAME, "search-snippet-view__placeholder")
        if not element:
            break

        ActionChains(driver).scroll_to_element(element[-1]).perform()
        time.sleep(2)

    html = driver.execute_script("return document.body.outerHTML;")
    with open("sber.html", "w", encoding="UTF-8") as file:
        file.write(html)
    return html


org_ids = []
list_new = {}


def get_file_page() -> str:
    '''
    Reads the contents of the file "sber.html" and returns its content.
    Returns: The HTML of the file "sber.html".
    '''
    with open("sber.html", encoding='utf-8') as f:
        html = f.read()
    return html


def scrape_reviews(driver: WebDriver, org_ids: List[Dict]) -> None:
    '''
        Scrapes reviews from Yandex Maps using Selenium and Beautiful Soup.
        :param driver: The Selenium WebDriver to use.
        :param org_ids: A list of dictionaries to store the scraped review data.
        '''
    count = 0
    for i in BeautifulSoup(html, "lxml").find_all("a", {"class": "search-snippet-view__link-overlay"}):
        org_id = i["href"].split("/")[-2]
        driver.get(f"https://yandex.ru/maps/org/gazprombank/{org_id}/reviews/")
        for _ in range(15):
            time.sleep(2)
            element = driver.find_elements(By.CLASS_NAME, "business-tab-wrapper")
            if not element:
                break

            ActionChains(driver).scroll_to_element(element[-1]).perform()
        soup = BeautifulSoup(driver.execute_script("return document.body.outerHTML;"), "lxml")
        reviews = soup.find_all("div", {"class": "business-reviews-card-view__review"})
        driver.get(f"https://yandex.ru/maps/org/gazprombank/{org_id}/")
        soup = BeautifulSoup(driver.execute_script("return document.body.outerHTML;"), "lxml")

        # Extract review data and store in dictionary
        for review in reviews:
            try:
                json_data: Dict[str, str] = {"name": review.find("span", {"itemprop": "name"}).text,
                                             "date": review.find("span", {"class": "business-review-view__date"}).text,
                                             "text": review.find("span", {"class": "business-review-view__body-text"}).text,
                                             "address": soup.find("div", {"class": "business-contacts-view__address"}).text,
                                             "rating": str(len(review.find_all("span", {"class": "_full"}))),
                                             }
            except Exception:
                # Skip over review if it can't be scraped
                print("DROPPED")
                time.sleep(100)
                continue
            if review.find("div", {"class": "cmnt-item-header__officiality-text"}):
                # If there is an official reply, add it to the review data
                json_data.update(reply_date=review.find("span", {"class": "cmnt-item-header__date"}).text,
                                 reply_text=review.find("span", {"class": "cmnt-item__message"}).text)
            count += 1
            if count % 50 == 0:
                # Dump review data to file every 50 reviews
                with open("yandex.json", "w") as file:
                    json.dump(org_ids, file)
            org_ids.append(json_data)
    # Dump all review data to file
    with open("yandex.json", "w") as file:
        json.dump(org_ids, file)


if __name__ == '__main__':
    driver = WebDriver()
    html = get_file_page()
    org_ids: List[Dict[str, str]] = []
    scrape_reviews(driver, org_ids)
    driver.quit()