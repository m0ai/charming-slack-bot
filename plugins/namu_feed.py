# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from rtmbot.core import Plugin, Job

import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Namu(Plugin):
    def register_jobs(self):
        time = 60*60
	job = NamuFeed(time)
    	self.jobs.append(job)

class NamuFeed(Job):
    def run(self, slack_client):
        baseurl = "https://namu.wiki"
        html_code = requests.get("https://namu.wiki/random").text
        soup = BeautifulSoup(html_code, 'html.parser')
        title = soup.find('h1', {'class' : 'title'})
        url = baseurl + title.a['href']
        return [["C5FJ1SN1X", "*{}* \n> {}".format(title.text.strip(), url)]]

    '''
    def process_message(self, data):
	if data['channel'].startswith("C847F9HTP"):
	    self.outputs.append(
		[data['channel'], 'from repeat1 "{}" in channel {}'.format(
		    data['text'], data['channel']
		)]
	    )
    '''
