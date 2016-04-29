from bs4 import BeautifulSoup
import requests
import time
import pymongo
client = pymongo.MongoClient('localhost', 27017)
test = client['test']
url_list = test['url_list']  # 负责存储每一个网页中的商品链接
item_info = test['item_info']  # 负责存储单个商品的信息

# ============================================抓取每个网页中的商品链接，不包括转转商品===============================


def get_links_from(channel, pages, who_sells=0):  # 0代表个人1代表商家
    # http://bj.58.com/pbdn/0/pn2/
    link_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(link_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    time.sleep(2)
    if soup.find('td', 't'):
        for link in soup.select('tr[logr] td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    else:
        pass
        # Nothing!
# get_links_from('http://bj.58.com/danche/',2)

# ====================================抓取单个商品的信息================================


def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = '404' in soup.find('script', type='text/javascript').get('src').split('/')
    # 判断该商品是否存在
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price.c_f50')[0].text
        date = soup.select('li.time')[0].text
        area = list(soup.select('span.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None
        item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area})
        print({'title': title, 'price': price, 'date': date, 'area': area})

# get_item_info('http://bj.58.com/pingbandiannao/25767625062314x.shtml')

# url='http://bj.58.com/shouji/24605954621114x.shtml'
# wb_data=requests.get(url)
# soup=BeautifulSoup(wb_data.text,'lxml')
# print(soup.prettify())


