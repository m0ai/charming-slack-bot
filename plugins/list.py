
from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from bs4 import BeautifulSoup
import os
import requests
filename = "list.file"
class List(Plugin):
    def is_exists(self):
        if os.path.exists(filename):
            return True
        self.outputs.append([data['channel'], u"can not found list file, please create a list (command : create list)"])
        return False

    def process_message(self, data):
        if data['channel'].startswith("C"):
            if data[u'text'] == u'help list':
                self.outputs.append([data['channel'], \
u"""
> show list\n
> create list\n
> add list\n
> del list
"""
                        ])

            if data[u'text'] == u'show list':
                if self.is_exists() is False: return
                output = ""
                with open(filename, 'rb') as f:
                    for index, line in enumerate(f.readlines()):
                        line = line.decode('utf8')
                        output += "> {} {}".format(index, line)
                self.outputs.append([data['channel'], u"{}".format(output)])
            if data[u'text'] == u'create list':
                with open(filename, 'wb') as f:
                    f.write('')
                self.outputs.append([data['channel'], u"> new list Create complete"])

            elif data[u'text'].startswith('add list'):
                if self.is_exists() is False: return
                new_data = "{}\n".format(data[u'text'][len('add list'):])
                with open(filename, 'a') as f:
                    f.write(new_data.encode('utf8'))
                self.outputs.append([data['channel'], u"> {} Add complete".format(new_data[:-1])])

            elif data[u'text'].startswith('del list'):
                if self.is_exists() is False: return
                del_index = int("{}".format(data[u'text'][len('del list'):]))
                lines = open(filename, 'rb').readlines()
                with open(filename, 'w') as f:
                    for index, line in enumerate(lines):
                        line = line.decode('utf8')
                        if index == del_index:
                            self.outputs.append([data['channel'], u"> {} Remove complete".format(line[:-1])])
                            continue
                        f.write(line.encode('utf8'))

