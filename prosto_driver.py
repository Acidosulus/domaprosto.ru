from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from bs4 import BeautifulSoup as BS
from lxml import html
import requests
from click import echo, style
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid

class WD:
    def init(self):
        self.site_url = 'https://doma-prosto.ru/'
        config = configparser.ConfigParser()


        
    def __init__(self):
        self.init()
        if False:
            chrome_options = webdriver.ChromeOptions()
            chrome_prefs = {}
            chrome_options.experimental_options["prefs"] = chrome_prefs
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--disable-notifications")
            #chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()

    def __del__(self):
        try:
            self.driver.quit()
        except: pass

    def Get_HTML(self, curl):
        if False:
            if os.path.isfile('response.html'):
                    echo(style('Загружен локальный файл: ', fg='bright_red') + style('response.html', fg='red'))
                    self.page_source = file_to_str('response.html')
            else:
                r = requests.get(curl)
                self.page_source = r.text
                str_to_file('response.html', self.page_source)
        else:
            #r = requests.get(curl, headers={'User-Agent': UserAgent().chrome})
            r = requests.get(curl)
            self.page_source = r.text
            #str_to_file(file_path="response.html", st = r.text)
            #self.driver.get(curl)
            #self.page_source = self.driver.page_source
            #return self.page_source
        return self.page_source

    def Get_List_Of_Links_On_Goods_From_Catalog(self, pc_link):
        echo(style('Список товаров каталога: ', fg='bright_yellow') + style(pc_link, fg='bright_white'))
        list_of_pages =  self.Get_List_of_Catalog_Pages(pc_link)
        echo(style('Стрaницы каталога: ', fg='bright_yellow') + style(str(list_of_pages), fg='green'))
        ll_catalog_items = []
        for link in list_of_pages:
            self.Get_HTML(link)
            soup = BS(self.page_source, features='html5lib')
            items = soup.find_all('a', {'class': 'product-list__name'})
            for item in items:
                lc_link = item['href']
                lc_link = (self.site_url[0:len(self.site_url)-1] if len(lc_link)>0 else '') + lc_link
                echo(style('Товар каталога: ', fg='bright_green') + style(lc_link, fg='green'))
                append_if_not_exists(lc_link, ll_catalog_items)
        return ll_catalog_items

    
    # def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
    # 	ll = []
    # 	lc = pc_href
    # 	ln_counter = 0
    # 	while len(lc)>0 and (lc!=pc_href or ln_counter==0):
    # 		ln_counter += 1
    # 		append_if_not_exists(lc, ll)
    # 		lc = self.Get_Next_Page_in_Catalog(lc)
    # 		if lc in ll: break
    # 	return ll
        
    def Get_List_of_Catalog_Pages(self, pc_href:str) -> list:
        self.Get_HTML(pc_href)
        soup = BS(self.page_source, features='html5lib')
        
        # Находим все ссылки в пагинации
        pagination_links = soup.find_all('a', href=lambda href: href and '?page=' in href)
        
        # Находим максимальный номер страницы
        max_page = 1
        for link in pagination_links:
            page_num = int(link['href'].split('=')[-1])
            if page_num > max_page:
                max_page = page_num
        
        # Генерируем список всех страниц
        ll = []
        print('max_page: ', max_page)
        for page_num in range(1, max_page + 1):
            if page_num == 1:
                ll.append(pc_href)
            else:
                ll.append(f"{pc_href}?page={page_num}")
        
        return ll

    def Get_Next_Page_in_Catalog(self, pc_link:str) -> str:
        echo(style('Find next page for: ', fg='bright_cyan') + style(pc_link,  fg='bright_green'))
        self.Get_HTML(pc_link)
        #self.Write_To_File(f'catalog_{uuid.uuid4()}.html')
        soup = BS(self.page_source, features='html5lib')
        paginator =soup.find_all('a',{'class':'page-link'})
        if len(paginator)<=0:
            return pc_link
        paginator = paginator[len(paginator)-1]
        if len(paginator['href'])>0:
            return self.site_url[0:len(self.site_url)-1] + paginator['href']



    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.page_source)
        file.close()


def Login():
    return WD()


#colorama.init()

#wd = Login()
#print(wd.Get_Next_Page_in_Catalog('https://doma-prosto.ru/category/dlya-detey/?page=2'))
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://doma-prosto.ru/category/dlya-detey/'))
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://klery.ru/maski-zashchitnye/'))

#print(wd.Get_List_of_Catalog_Pages('https://klery.ru/maski-zashchitnye/'))
