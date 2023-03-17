from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import json
import re

headers = {'User Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

"""This is extracting data from purely just looking at whether something has headline within it"""
""" headlines = re.findall(r'"headline":"(.*?)"', text)
print(headlines) """


def fetchCNN(cnnMainLink):
    # This code makes a request to the CNN main Tech site to get the whole document page
    url = cnnMainLink
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    cnn_links = []
    cnn_href_array = []
    # Gathers all the links from the page of news articles
    for link in soup.find_all('a', class_='container__link container_lead-plus-headlines-with-images__link'):
        link_info = {}
        link_info['text'] = link.text
        link_info['href'] = link.get('href')
        cnn_links.append(link_info)
        cnn_href_array.append(link['href'])

    for link in cnn_links:
        print("The Link --> ", link)

    print(cnn_href_array)
    cnn_articles = []
    # Gathers all the data of the articles and stores them in cnn_articles
    for hrefLink in cnn_href_array:
    
        url = "https://cnn.com"+hrefLink
        print(url)
        response=requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', {'id': 'maincontent'}).text
        title = title.replace('\n', "")
        article_content = soup.find_all('div', class_="article__content")
        main_text = ""
        for content in article_content:
            main_text += content.get_text()
            main_text = main_text.replace('\n', '')
            

        # Create a dictionary with the article URL and main text, and add it to the cnn_articles list
        article = {"url": url, "title": title, "main_text": main_text}
        cnn_articles.append(article)

        print(cnn_articles)

    return cnn_articles



def fetchTechCrunchSections(techCrunchLink):
    url = techCrunchLink
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tech_crunch_links = []
    for link in soup.find_all('a', class_="post-block__title__link"):
       # print(link.get('href'))
        href = link.get('href')
        tech_crunch_links.append({'href': href})
        href_response = requests.get(href)
        soup_for_articles = BeautifulSoup(href_response.text, "html.parser")
        title = soup_for_articles.find('h1', class_="article__title").text
        article_content = soup_for_articles.find("div", class_="article-content").text
        article_content = article_content.replace("\n", "")
        article_content = article_content.replace("\xa0", "")
        tech_crunch_links.append({'title': title})
        tech_crunch_links.append({"main_text": article_content})

    print(tech_crunch_links)
   

def fetchGizmodo(gizmodoUrl):
    url = gizmodoUrl
    response = requests.get(url)
    soup= BeautifulSoup(response.text, 'html.parser')
    gizmodo_articles = []
    for link in soup.find_all('a', class_="sc-1out364-0 hMndXN sc-1pw4fyi-5 dmviYs js_link"):
        href= link.get('href')
        gizmodo_articles.append({'href': href})
        href_response = requests.get(href)
        soup_for_articles = BeautifulSoup(href_response.text, "html.parser")
        title_tag = soup_for_articles.find('h1', class_="sc-1efpnfq-0 joZwQS")
        title = title_tag.get_text() if title_tag else ''
        article_content = soup_for_articles.find("div", class_="xs32fe-0 iOFxrO js_post-content").find_all('p')
        main_text = ""
        for p in article_content:
            main_text += p.get_text()
        gizmodo_articles.append({'title': title, 'main_text': main_text})

    print(gizmodo_articles)

    
    # print(gizmodo_articles)
        


fetchGizmodo("https://gizmodo.com/science")



cnn_url_lists = ["adadf","https://www.cnn.com/business/media", "https://www.cnn.com/business/tech", "https://www.cnn.com/business", "https://www.cnn.com/business/success"]
    

# fetchTechCrunchSections("https://techcrunch.com/category/startups/")
""" for url in cnn_url_lists:
    try:
        fetchCNN(url)

    except Exception as e:
        print('Error: ', e) """

