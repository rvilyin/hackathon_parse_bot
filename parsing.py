import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime



def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(year, month, day):
    url = f'https://kaktus.media/?lable=8&date={year}-{month}-{day}&order=time'
    html = get_html(url)
    soup = get_soup(html)
    articles_block = soup.find('div', class_='Tag--articles')
    articles = articles_block.find_all('div', class_='Tag--article')
    return articles

def get_data2():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    articles = get_data(year, month, day)
    
    if len(articles) < 20:
        articles2 = get_data(year, month, day-1)
        articles.extend(articles2[:20-len(articles)])

    return articles

def get_description(article):
    url = article.find('a', class_='ArticleItem--name').get('href')
    html = get_html(url)
    soup = get_soup(html)
    try:
        article_text = soup.find('div', class_='BbCode')
        paragraphs = article_text.find_all('p')
        s = ''
        for paragraph in paragraphs:
            s1 = paragraph.text.strip('" ')
            s += f'{s1}\n'
    except AttributeError:
        s = 'Нет описания'
    return s


def get_titles(articles):
    l = []
    for article in articles:
        try:
            title = article.find('a', class_='ArticleItem--name').text.strip()
        except AttributeError:
            title = "Нет названия"
        l.append(title)
    return l



