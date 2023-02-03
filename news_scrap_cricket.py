import requests
import  pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os
import sys
from fpdf import FPDF



def get_all_news(soup):
    all_news = soup.find_all('div', {'class': 'xl:ds-pt-[10px] xl:ds-ml-[120px] xl:ds-w-[600px]'})
    if all_news != []:
        # print(all_news)
        for news1 in all_news:
            result_news = []
            club = news1.find_all('div')
            if club != []:
                for data in club:
                    result_news.append(data.text)
        information = ' '.join(result_news)
    else: 
        information = []
    return information
        
def get_url(soup):
    all_url = []
    all_section = soup.find_all('div', {'class': 'ds-p-0'})
    for section in all_section:
        url_links = section.find_all('a')
        for url_link in url_links:
            first_url = 'https://www.espncricinfo.com'
            data = url_link['href']
            data = first_url+data
            all_url.append(data)
    return all_url

def data_set(no_of_pages):
    data_set = pd.DataFrame(columns=['News', 'Category'])
    news_data = []
    category_data = []
    
    for i in range(1,no_of_pages+1):
        print(i)
        url = f'https://www.espncricinfo.com/cricket-news?page={i}'

        # initially get the page from the url and form the content extract all teh things peoperly so  page is extracted
        page = requests.get(url)
        # Soup is created where all the content is parsed as html so it can be extracted as seen in webpage
        soup = BeautifulSoup(page.content, 'html.parser')

        label_urls = get_url(soup)
        for label_url in label_urls:
            print(label_url)
            page1 = requests.get(label_url)
            
            soup1 = BeautifulSoup(page1.content, 'html.parser')
            
            news  = get_all_news(soup1)
            news_data.append(news)
            category_data.append('Cricket')

    data_set = pd.DataFrame({'News': news_data, 'Category': category_data})
    data_set.to_csv('Dataset.csv', mode='a', header=False)


os.system('cls')
no_of_pages = int(input('Enter Number of page you want to scrap: '))
data_set(no_of_pages)





