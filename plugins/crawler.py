
from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from bs4 import BeautifulSoup
import requests

class Crawler(Plugin):
    def process_message(self, data):
        if data['channel'].startswith("C"):
            if data[u'text'] == u'naver':
                url = "http://www.naver.com/"
                r  = requests.get(url)
                soup = BeautifulSoup(r.text , 'html.parser')
                _str = ""
                for rank_list in soup.find_all('a', {'class' : 'ah_a', 'data-clk' : 'lve.keyword'},):
                    rank = rank_list.find('span', 'ah_r').text
                    word = rank_list.find('span', 'ah_k').text
                    url = rank_list['href']
                    if int(rank) > 10: break
                    #print rank.text , word.text, rank_list['href']
                    _str = _str + "> {} {}\n".format(rank, word)
                self.outputs.append([data['channel'], u"{}".format(_str)])

