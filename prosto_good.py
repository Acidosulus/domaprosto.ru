from my_library import *
from prosto_driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style
from my_library import sx
import json
# from rich import print

def poiskpers(url):
    geourl = '{0}'.format(quote(url))
    return geourl

class Good:
    def __init__(self, ol:WD, pc_good_link, pc_price:str):
        pc_good_link = pc_good_link.replace(r'amp;', '')
        self.pictures = []
        self.sizes = []
        self.prices = []
        self.color = ''
        self.article = ''
        self.name = ''
        self.description= ''
        self.price = ''
        self.brand = ''
        echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
        ol.Get_HTML(pc_good_link)
        soup = BS(ol.page_source, features='html5lib')
        
        ## remove additinal goods miniatures from the page bottom
        while soup.find('div',{'class':'s-related-products'})!=None:
            soup.find('div',{'class':'s-related-products'}).replace_with('')

        self.name = soup.find('h1').text.strip()

        try:
            images = soup.find_all('img',{'class':"owl-lazy product-gallery-main__el-photo"})
            for image in images:
                lc_picture_link = image['data-src']
                if 'data:image' not in lc_picture_link:
                    append_if_not_exists('https://doma-prosto.ru' + lc_picture_link, self.pictures)
        except:
            pass
        

        # for picture in pictures:
        #     if 'data:image' not in picture:
        #         append_if_not_exists('https://doma-prosto.ru' + picture['href'], self.pictures)
        # if len(self.pictures)==0:
        try:	
            for img in soup.find('div', {'class':'product-gallery-main__el-photo'}).find_all('img'): ## pictures from description
                if 'data:image' not in img['src']:
                    append_if_not_exists(img['src'], self.pictures)
        except:
            pass


        try: self.description =  soup.find('div', {'itemprop':'description'}).text.replace(chr(10),' ').strip()
        except: pass

        try: self.description += (' '+soup.find('div', {'class':'s-product-description s-user-content'}).text.replace(chr(10),' ')).strip()
        except: pass

    
        object = sx(
            sx(
                ol.page_source,
                '<script>$(function(){Price.addCurrency(',
                ');</script>',
                1
            ),
            "new Product('#cart-form',",
            ");",
            1
        )

        object = "{"+sx(object,"skus: {", "}},")+"}}"

        with open('object.txt', 'w', encoding='utf-8') as file:
            file.write(object)
        
        data = json.loads(object)

        # print(data)
        # print(data.keys())
        for key in data.keys():
            # print(key)
            # print(data[key])
            section = data[key]
            if section.get('count')>0:
                self.sizes.append((section.get('name') if len(section.get('name'))>0 else '*'))
                self.prices.append(section.get('price'))

