import requests
from bs4 import BeautifulSoup


def rb_parser():
    base_url = 'https://rb.ru'
    url = base_url + '/tag/business/'
    news = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find_all('div', {'class': 'news-item__text'})
    for item in content:
        h2 = item.find('h2')
        a = h2.find('a')
        news_url = a['href']
        title = a.text
        description = item.find('div', {'class': 'news-item__details'}).text
        news.append((base_url + news_url, title + ' ' + description))
    return news
