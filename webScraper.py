import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import re


ua = UserAgent()
headers = {'User Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
randomHeaders = {'User-Agent': ua.random}

"""This is extracting data from purely just looking at whether something has headline within it"""
""" headlines = re.findall(r'"headline":"(.*?)"', text)
print(headlines) """


def fetchCNN(cnnMainLink, category):
    # This code makes a request to the CNN main Tech/Business site to get the whole document page
    url = cnnMainLink
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    cnn_links = []
    # Gathers all the links from the page of news articles
    for link in soup.find_all('a', class_='container__link container_lead-plus-headlines-with-images__link'):
        link_info = {}
        link_info['text'] = link.text
        link_info['href'] = link.get('href')
        cnn_links.append(link_info)
        # cnn_href_array.append(link['href'])


    cnn_articles = []
    # Gathers all the data of the articles and stores them in cnn_articles
    for hrefLink in cnn_links:
    
        url = "https://cnn.com"+hrefLink['href']
        #print(url)
        response=requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('h1', {'id': 'maincontent'})
        title = title_tag.text if title_tag else ''
        title = title.replace('\n', "")
        article_content = soup.find_all('div', class_="article__content")
        main_text = ""
        for content in article_content:
            main_text += content.get_text()
            main_text = main_text.replace('\n', '')
            main_text = main_text.encode('ascii', 'ignore').decode('ascii')
            
            

        # Create a dictionary with the article URL and main text, and add it to the cnn_articles list
        article = {"url": url, "title": title, "main_text": main_text}
        cnn_articles.append(article)

        category_dict = {category: cnn_articles}


        json_cnn = json.dumps(category_dict)

        
    return json_cnn



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

    return(tech_crunch_links)
   

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




def fetchYahooFinance(link, type):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    a_tags = soup.find_all(
        'a', class_="js-content-viewer Fw(b) Td(n) wafer-destroyed")
    print(a_tags)
    hrefs = [a.get('href') for a in a_tags]
    yahoo_articles = []
    for href in hrefs:
        print(href)
        href_response = requests.get(href)
        soup_for_articles = BeautifulSoup(href_response.text, "html.parser")
        title_tag = soup_for_articles.find('h1', {'data-test-locator': 'headline'}).get_text
        article_content_div = soup_for_articles.find( 'div', class_= 'caas-body')
        paragraphs = article_content_div.find_all('p')
        article = {'href': href, 'title': title_tag,
                   'main_text': [p.text for p in paragraphs]}
        yahoo_articles.append(article) 
    return yahoo_articles 
    
   
    
        
def fetchInvestopedia(link, type):
    response = requests.get(link)
    soup= BeautifulSoup(response.text, 'html.parser')
    soup_div = soup.find('div', class_="comp home-hero__wrapper mntl-block")
    soup_links = soup_div.find_all('a')
    invest_articles = []
    for link in soup_links:
        href = link.get('href')
        href_response = requests.get(href)
        soup_for_articles = BeautifulSoup(href_response.text, "html.parser")
        title_tag = soup_for_articles.find( 'h1', class_="comp article-heading mntl-text-block").text
        article_content_div = soup_for_articles.find('div', class_= 'comp article-body mntl-block')
        article_body_content_div = article_content_div.find(
            'div', class_='comp article-body-content mntl-sc-page mntl-block')
        paragraphs = article_body_content_div.find_all('p')

        article = {'href': href, 'title': title_tag,
                   'main_text': [p.text for p in paragraphs]}
        invest_articles.append(article)
        """ for tag in article_content_div.children:
            if tag.name in ['h2', 'h3']:
                current_heading = tag.text
            elif tag.name == 'p' and current_heading:
                content_list.append(
                    {'heading': current_heading, 'main_text': tag.text})
                current_heading = None
        article = {'href': href, 'title': title_tag, 'content': content_list}
        invest_articles.append(article) """
    return invest_articles






cnn_url_lists = ["adadf","https://www.cnn.com/business/media", "https://www.cnn.com/business/tech", "https://www.cnn.com/business", "https://www.cnn.com/business/success"]
    

# fetchTechCrunchSections("https://techcrunch.com/category/startups/")
""" for url in cnn_url_lists:
    try:
        fetchCNN(url)

    except Exception as e:
        print('Error: ', e) """

