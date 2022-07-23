from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import re
from time import sleep
import json
from serpapi import GoogleSearch
import requests
import os


cwd = os.getcwd()
today = date.today()
d = today.strftime("%B %d, %Y")

# search = input("Enter item to be searched: ")

with open('{0}\Product names.json'.format(cwd), 'r') as Products:
    names = json.load(Products)
    company = list(names)
    prod = list(names.values())


geoBlocked = webdriver.FirefoxOptions()
geoBlocked.set_preference("geo.prompt.testing", True)
geoBlocked.set_preference("geo.prompt.testing.allow", False)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

try:
    os.makedirs("Output/{0}".format(d))
except FileExistsError:
    # directory already exists
    pass


# -----------------
#       Amazon
# -----------------

def AmazonScraper(search, items):
    count = 0

    # with open('regions.json', 'r') as url_file:
    #    file_url = json.load(url_file)
    #   loc = list(file_url)
    #  urls = list(file_url.values())

    # search = 'Microsoft 365'
    search_query = search.replace(' ', '+')

    url = "https://www.amazon.com/"

    base_url = url + 's?k={0}'.format(search_query)

    print('Page {0} ...'.format(base_url + '&page=1'))
    response = requests.get(
        base_url + '&page=1', headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    results = soup.find_all(
        'div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            price = result.find(
                'span', {'class': 'a-offscreen'}).text
            product_url = url + result.h2.a['href']
            items.append([product_name, price, product_url])
        except AttributeError:
            continue
    sleep(1.5)

    name = 'Amazon USA '
    count = count + 1
    return name


# -----------------
#     BEST BUY
# -----------------


def BestBuyScraper(search, items):

    srch_fn = browser.find_element_by_id('gh-search-input')
    srch_fn.send_keys(search)

    sleep(1.5)

    search_button = browser.find_element_by_class_name('header-search-icon')
    search_button.click()

    page_src = browser.page_source

    soup = BeautifulSoup(page_src, 'lxml')

    results = soup.find_all('li', {'class': 'sku-item'})

    url = 'https://www.bestbuy.com'

    for result in results:
        product_name = result.h4.text
        try:
            price = result.find(
                'div', {'class': 'priceView-hero-price'}).text
            price = '$' + re.search(r"\d+\.\d+", price)[0]
            product_url = url + result.h4.a['href']
            items.append([product_name, price, product_url])
        except AttributeError:
            continue
        sleep(1.5)

    name = 'BestBuy '
    browser.back()
    return name


# -----------------
#       HP
# -----------------


def HPScraper():

    count = 0

    links = {
        "HP Omen": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345619993322&urlLangId=&quantity=1',
        "HP Spectre": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620102827&urlLangId=&quantity=1',
        "HP Envy": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620102819&urlLangId=&quantity=1',
        "HP Pavilion": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620102824&urlLangId=&quantity=1',
        "HP Pavilion Gaming Desktop": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345619629318&urlLangId=&quantity=1',
        "HP Omen Desktop": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620106819&urlLangId=&quantity=1',
        "HP Envy Desktop": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345619965320&urlLangId=&quantity=1',
        "HP Victus Desktop": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620235323&urlLangId=&quantity=1'
    }

    urls = list(links.values())
    names = list(links)

    for link in urls:
        items = []
        browser = webdriver.Firefox(options=geoBlocked)
        browser.get(link)
        page_src = browser.page_source

        soup = BeautifulSoup(page_src, 'lxml')

        results = soup.find_all('div', {'class': 'configure-option'})
        for result in results:
            for cat in result:
                for sub_cat in cat:
                    try:
                        price = sub_cat.find(
                            'div', {'class': 'radio-info price'}).text
                        price = price.replace('+', '').lstrip()
                        name = sub_cat.find(
                            'div', {'class': 'radio-label'}).text
                    except:
                        continue
                    items.append([name, price, link])

        results = soup.find_all(
            'div', {'class': 'configure-option', 'data-path': "39R27AV.CreatorSoftware"})
        for result in results:
            for cat in result:
                try:
                    name = cat.find(
                        'span', {'class': "Checkbox-module_content__3j9aq"}).text
                    price = cat.find(
                        'div', {'class': "PriceBlock-module_salePrice___Hf7T"}).text
                    name = name.replace(price, "")
                except:
                    continue
                items.append([name, price, link])

        browser.quit()

        item_req = [
            item for item in items for app in company if app in item[0]]

        file_name = names[count] + ' ' + d
        df = pd.DataFrame(item_req, columns=[
                          'product', 'price', 'url'])
        df.to_excel(
            '{}/Output/{}/{}.xlsx'.format(cwd, d, file_name), sheet_name='sheet1', index=False)
        count = count + 1


# -----------------
#      Walmart
# -----------------


def WalmartScraper(search, items):
    engine = "walmart"

    params = {
        "api_key": "dd8a3a3e696b0c8ab7db5cbb3952bc2577623e3d5ec49a08e0076fd7a136da85",
        "engine": engine,
        "query": search
    }
    # api_key is linked to account, 100 searches per month, search serp api and replace api_key with own api key
    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results["organic_results"]:
        product_title = result['title']
        product_link = result['product_page_url']
        offer = result['primary_offer']
        price = offer['offer_price']

        items.append({
            'product': product_title,
            'link': product_link,
            'price': price
        })

    name = 'Walmart '
    return name


def file_writer(items, company_number, nm):
    res = [i for n, i in enumerate(items) if i not in items[n + 1:]]
    df = pd.DataFrame(res, columns=['product', 'price', 'product url'])
    file_name = nm + company[company_number] + ' ' + d
    df.to_excel(
        '{}/Output/{}/{}.xlsx'.format(cwd, d, file_name), sheet_name="Sheet_1", index=False)

# Best Buy Output generator


company_number = 0

for item in prod:
    items = []
    browser = webdriver.Firefox(options=geoBlocked)

    browser.get('https://www.bestbuy.com/site')

    eng = browser.find_element_by_class_name("us-link")
    eng.click()

    print("Best Buy USA")

    for search in item:
        nm1 = BestBuyScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1
    browser.quit()

# Amazon Output generator

company_number = 0

for item in prod:
    items = []
    for search in item:
        nm1 = AmazonScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1

# Walmart Output generator

company_number = 0

for item in prod:
    items = []
    for search in item:
        nm1 = WalmartScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1


BestBuyScraper(search)
HPScraper()
