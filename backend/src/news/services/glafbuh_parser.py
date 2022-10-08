import time

from bs4 import BeautifulSoup
from selenium import webdriver


def glafbuh_parser():
    base_url = 'https://www.glavbukh.ru'
    url = base_url + '/news/'
    news = []

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Remote(
        'http://selenium:4444/wd/hub', options=options
    )
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    div = soup.find_all('div', {'class': 'news-list__item'})
    for item in div:
        if item:
            p = item.find('p')
            if p:
                text = item.find('p').text
                if text:
                    span = item.find('span')
                    a = span.find('a')
                    href = a['href']
                    news.append((base_url + href, text))
    return news
