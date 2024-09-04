from my_library import *
from prosto_driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style
from my_library import sx

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

		pictures = soup.find_all('a',{'class':'swiper-slide'})
		for picture in pictures:
			if 'data:image' not in picture:
				append_if_not_exists('https://doma-prosto.ru' + picture['href'], self.pictures)
		if len(self.pictures)==0:
			try:
				lc_picture_link = soup.find('img',{'class':'product-gallery-main__el-photo'})['src']
				if 'data:image' not in lc_picture_link:
					append_if_not_exists('https://doma-prosto.ru' + lc_picture_link, self.pictures)
			except:
				pass
		try:	
			for img in soup.find('div', {'class':'s-product-description s-user-content'}).find_all('img'): ## pictures from description
				if 'data:image' not in img['src']:
					append_if_not_exists(img['src'], self.pictures)
		except:
			pass

		try: self.description =  soup.find('div', {'itemprop':'description'}).text.replace(chr(10),' ').strip()
		except: pass

		try: self.description += (' '+soup.find('div', {'class':'s-product-description s-user-content'}).text.replace(chr(10),' ')).strip()
		except: pass

	
		# for item in soup.find('div',{'itemprop':'offers'}):
		# 	if 'meta content' in str(item) and 'itemprop="availability"' and 'offerCount' not in str(item):
		# 		self.sizes.append(sx(str(item), 'meta content="','"'))
		# 		print(str(item	))
		# if len(self.sizes)==0:
		# 	self.sizes=['*']
		
		# offers = soup.find_all(itemprop="offers", itemtype="http://schema.org/Offer")
		# items = []

		# for offer in offers:
		# 	color = offer.find("meta", {"itemprop": "name"})["content"]
		# 	price = offer.find("meta", {"itemprop": "price"})["content"]
		# 	items.append({"color": color, "price": price})
		# print('-------')
		# print(items)
		# print('-------')
		
		# block = soup.find('div',{'class':'b-product-skus'})
		blocks = soup.find_all('div',{'class':'s-sku-item'})
		for block in blocks:
			if 'data-disabled="1"' not in str(block):
				self.prices.append(block.find('input')['data-price'].replace(',','.').replace(' ','').strip())
				self.sizes.append(block.text.strip())

		if len(self.prices)==0:
			try: # more than one color and price
				prices = soup.find_all('label')
				if len(prices)==0:
					raise Exception('Zero count of prices')
				for oprice in prices:
					if 'class="disabled"' in str(oprice):
						break # don't allowed for purchase
					name = oprice.find('span',{'itemprop':'name'}).text.strip()
					price = oprice.find('span',{'class':'price tiny nowrap'}).text.replace('₽','').strip()
					self.sizes.append(name)
					self.prices.append(price)
			except: # one price and no colors
				try:
					price = soup.find('div', {'class':'price'}).text.replace('₽','').strip()
				except:
					price = soup.find('span', {'class':'price'}).text.replace('₽','').strip()
				self.sizes.append('*')
				self.prices.append(price)