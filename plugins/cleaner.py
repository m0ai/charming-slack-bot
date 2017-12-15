# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
import os
import re
import random
import sqlite3
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
prob_db = "prob.sqlite"
score = 3
class Cleaner(Plugin):
        # {u'source_team': u'T5G84C005', u'text': u'\u314b\u314b', u'ts': u'1511921630.000236', u'user': u'U5G85LAN9', u'team': u'T5G84C005', u'type': u'message', u'channel': u'C5FJ1SN1X'}
    def get_userinfo(self, name):
        url = "https://slack.com/api/users.info?token={}&&user={}"\
                .format(os.environ['SLACK_BOT_TOKEN'], name)
        data = requests.get(url).text
        return json.loads(data)['user']

    def add_get_args(self, url, data=dict()):
        for key in data.keys():
            url = url + "{}={}&".format(key, data[key])
        return url

    def remove_chat_history(self, data, remove_count=10):
        if remove_count > 69:
            self.outputs.append([data['channel'], u"너무 많아~"])
        base_url = "https://slack.com/api/channels.history?"
        url = "https://slack.com/api/channels.history?token={}&channel=C5FJ1SN1X&pretty=1".format(os.environ['SLAKC_BOT_TOKEN'])
        send_data =  dict()
        send_data['token'] = os.environ['SLACK_BOT_TOKEN']
        send_data['channel'] = data['channel']
        send_data['count'] = remove_count
        url = self.add_get_args(base_url, send_data)
        r = requests.get(url)
        json_dict = json.loads(r.text)
        if json_dict['ok'] is True:
            for msg_info in json_dict['messages']:
                delete_url = "https://slack.com/api/chat.delete?"
                send_data['token'] = os.environ['SLACK_BOT_TOKEN']
                send_data['channel'] = data['channel']
                send_data['ts'] = msg_info['ts']
                url = self.add_get_args(delete_url, send_data)
                print(delete_url)
                r = requests.get(url)
                print(r.text)

    def process_message(self, data):
        if data['channel'].startswith("C"):
            if data['text'] == u'clean':
                self.remove_chat_history(data)
                #self.outputs.append([data['channel'], u"뀨".format(hint)])
            elif data['text'].find(u'퇴근') > -1 :
                self.remove_chat_history(data, remove_count=1)

            elif data['text'].startswith(u"clean"):
                try:
                    remove_count = int(data['text'].split()[1])
                    self.remove_chat_history(data, remove_count)
                except:
                    self.outputs.append([data['channel'], u"뀨"])


