import os
import re
import requests
from bs4 import BeautifulSoup as bs


def find_articles(num_pages, article_type):
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
    for i in range(1, num_pages + 1):
        resp = requests.get(url + str(i))
        soup = bs(resp.text, "html.parser")
        articles = soup.find_all("article", class_="u-full-height c-card c-card--flush")
        saved_articles = []
        os.makedirs("Page_" + str(i), exist_ok=True)
        for article in articles:
            type_article = article.find('span', class_="c-meta__type").text
            name_article = article.find('a', class_="c-card__link").text
            if type_article == article_type:
                replace_name_article = name_article.replace(' ', '_')
                replace_name_article_res = re.sub(r'[^\S,?,":"]', '', replace_name_article)
                saved_articles.append(replace_name_article_res + ".txt")
                link = article.a.get("href")
                url_article = 'https://www.nature.com' + link
                content_link = requests.get(url_article).text
                soup_content = bs(content_link, "html.parser")
                content = soup_content.find("div", class_="c-article-body").text
                with open(os.path.join("Page_" + str(i), replace_name_article_res + '.txt'), 'w', encoding='utf-8') as f:
                    f.write(content)


num_pages = int(input())
article = input()
find_articles(num_pages, article)

print('Saved all articles.')
















