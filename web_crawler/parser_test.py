import requests
from bs4 import BeautifulSoup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "get_mask.settings")

import django
django.setup()

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
	# json.dump(data, json_file)

from mask.models import CoupangData

def parse_coupang():
	headers = {
	    'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
	    }
	#req = requests.get('https://www.coupang.com/np/campaigns/4236?listSize=60&brand=&offerCondition=&filterType=rocket%2Crocket_wow%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=1%23attr_ic_64042%2417801%2C17799attr_2641%2416309%40DEFAULT&rating=0&rocketAll=true', headers=headers)
	req = requests.get('https://www.coupang.com/np/campaigns/4236?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=bestAsc&filter=1%23attr_ic_64042%2417799attr_2641%2416309%40DEFAULT&rating=0', headers=headers)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	data = {}
	items = soup.find_all('a', class_='baby-product-link', limit=5)
	for item in items:
		link_url = 'https://www.coupang.com/' + item.get('href')
		item_id = item.get('data-product-id')
		next_req = requests.get(link_url, headers=headers)
		next_html = next_req.text
		next_soup = BeautifulSoup(next_html, 'html.parser')
		stock_info = next_soup.find(class_='oos-label') 
		if stock_info is None:
			data[item_id] = link_url
			print(link_url)
		else :
			print('out of stock')
	return data
		
if __name__=='__main__':
	mask_data_dict = parse_coupang()
	for i, l in mask_data_dict.items():
		CoupangData(item_id=i, is_oos=True, link=l).save()
