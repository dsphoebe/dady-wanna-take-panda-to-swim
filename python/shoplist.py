# coding=utf-8
from bs4 import BeautifulSoup
import requests


PAGES = 50
URL = 'https://www.dianping.com/search/keyword/2/0_%E4%BA%B2%E5%AD%90%E6%B8%B8%E6%B3%B3'

returnList = []


def get_dianping():
    for num in range(1, PAGES):
        url = URL if num == 1 else '%sp%s' % (URL, num)
        get_shop(url)


def get_shop(scenic_url):
    proxies = {
        'http': '45.77.25.235:8081',
    }
    headers = {
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/39.0.2171.95 Safari/535.19',
        'Accept-Encoding': 'gzip'
    }
    cookies = {
        'cy': '835',
        'cye': 'guanyun',
        '_lxsdk_cuid': '16426247fafc8-0cf040f6fc4a118-4c312b7b-\
            100200-16426247fafc8',
        '_lxsdk': '16426247fafc8-0cf040f6fc4a118-4c312b7b-100200-\
            16426247fafc8',
        '_hc.v': '7b5b3de6-776c-46d2-e7d3-e468d13446dc.1529648284',
        '_dp.ac.v': 'c584c92c-95aa-4220-a4e0-bb40878ae863',
        'ua': '15366181451',
        's_ViewType': '10', 
        '_lxsdk_s': '1644ec042ce-f7f-0ee-489%7C%7C1176',
        'cityInfo': '%7B%22cityId%22%3A835%2C%22cityEnName%22%3A%22guanyun\
            %22%2C%22cityName%22%3A%22%E7%81%8C%E4%BA%91%E5%8E%BF%22%7D',
        '__mta': '146585483.1530329665619.1530330562343.1530330863738.6',
        'ctu': '4a3974cdf5b2e5b0fd3b2d9a6ec23a7d48c74ae4f2a36e\
            72bfed34b59b322f331e42d186b52cd0db5fa5a045e40f22d4',
        'dper': '79ff66a7e0fc79b70c8ac58013ca79eda9a3b87d62b5ad\
            42a670e8244ddcbba0ee1a751db6a8e0ff39608623d5575eb1e6f823\
            7e50713a9455f35c1d81ef75cbed81c68fc95315a4c2dde5930e0a840\
            d14eddc61aee31c213f59c602aba3d13d',
        'll': '7fd06e815b796be3df069dec7836c3df',
        '_lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorgani'
    }

    requests.adapters.DEFAULT_RETRIES = 5

    s = requests.session()
    s.keep_alive = False

    r = requests.get(
        scenic_url, headers=headers, cookies=cookies, proxies=proxies)

    soup = BeautifulSoup(r.text, 'lxml')

    shoplist = soup.select('.shop-list ul li')

    for one in shoplist:
        title = one.select_one('.tit h4')
        title = title.get_text().strip()
        print ('title:%s' % (title))

        addr_tag = one.select_one(
            '.tag-addr a[href^="http://www.dianping.com/beijing/ch0"] .tag')
        addr_tag = addr_tag.get_text().strip()
        addr = one.select_one('.tag-addr .addr')
        addr = addr.get_text().strip()
        print ('addr:%s %s' % (addr_tag, addr))

        star = one.select_one('.txt .comment span')
        star = star['class'][1][7:8]
        print ('star:%s' % (star))

        price = one.select_one('.svr-info .si-deal a[target="_blank"]')
        price = price.get_text().strip() if price else u'没有团购信息'
        print ('price:%s' % (price))

        returnList.append([title, addr, star, price])

        print ('=============================================================')

    return returnList


if __name__ == '__main__':
    get_dianping()
