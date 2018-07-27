# coding: utf-8
__author__ = 'zhy'

import requests
from bs4 import BeautifulSoup
import multiprocessing
import time

success_num=0

CONSTANT=0
def getProxyIp():
    global CONSTANT
    proxy = []
    for i in range(1, 12):
        print i
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Ubuntu Chromium/44.0.2403.89 '
                                'Chrome/44.0.2403.89 '
                                'Safari/537.36'}
        r = requests.get('http://www.xicidaili.com/nt/{0}'.format(i), headers=header)

        html = r.text
        soup = BeautifulSoup(html)
        table = soup.find('table', attrs={'id': 'ip_list'})
        tr = table.find_all('tr')[1:]

        # 解析得到代理ip的地址，端口，和类型
        for item in tr:
            tds = item.find_all('td')
            print tds[1].get_text()
            temp_dict = {}
            kind = tds[5].get_text().lower()
            # exit()

            if 'http' in kind:
                temp_dict['http'] = "http://{0}:{1}".format(tds[1].get_text(), tds[2].get_text())
            if 'https' in kind:
                temp_dict['https'] = "https://{0}:{1}".format(tds[1].get_text(), tds[2].get_text())

            proxy.append(temp_dict)
    return proxy


def brash(proxy_dict):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Ubuntu Chromium/44.0.2403.89 '
                            'Chrome/44.0.2403.89 '
                            'Safari/537.36'}
    # header ={'Mozilla/5.0 (Linux; Android 4.4.2; 2014501 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/25.0)'}                        
    try:
        # http://blog.csdn.net/zhy421202048/article/details/50935685
        # http://blog.csdn.net/zhy421202048/article/details/50937423
        r = requests.get("http://blog.csdn.net/zhy421202048/article/details/51499260", headers=header, proxies=proxy_dict, timeout=10)
    except Exception, e:
        print "failed"
        # CONSTANT +=1
    else:
        print "successful"
    time.sleep(0.5)
    return None


if __name__ == '__main__':
    i = 0
    t = 0
    final = input()  # 输入数字代表要获取多少次代理ip
    while t < final:
        t += 1
        proxies = getProxyIp()  # 获取代理ip网站上的前12页的ip
        # print CONSTANT
        for i in range(5):
            i += 1
            pool = multiprocessing.Pool(processes=32)
            results = []
            for i in range(len(proxies)):
                results.append(pool.apply_async(brash, (proxies[i],)))
            for i in range(len(proxies)):
                results[i].get()
            pool.close()
            pool.join()
        i = 0
        time.sleep(20)

