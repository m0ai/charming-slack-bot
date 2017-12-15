from __future__ import print_function
from rtmbot.core import Plugin
import json
import requests

class CryptocoinPlugin(Plugin):
    def command_mvc(self, data):
        command = data['text']
        if command == "coin":
            coin = self.parse_from_coinone()
            result = "BTC : {btc}\n"\
                    "ETH : {eth}\n"\
                    "ETC : {etc}\n"\
                    "LTC : {ltc}\n"\
                    "QTUM: {qtum}\n"\
                    "BCH: {bch}\n"\
                    "BTG: {btg}\n"\
                    "IOTA : {iota}\n"\
                    "XRP : {xrp}\n".format(btc=coin['BTC'],
                                            eth=coin['ETH'],
                                            etc=coin['ETC'],
                                            xrp=coin['XRP'],
                                            btg=coin['BTG'],
                                            bch=coin['BCH'],
                                            iota=coin['IOTA'],
                                            qtum=coin['QTUM'],
                                            ltc=coin['LTC'])
	    self.outputs.append([data['channel'], result])

    def process_message(self, data):
        if data['channel'].startswith("C"):
            self.command_mvc(data)

    def parse_from_coinone(self):
	jdat = requests.get("https://api.coinone.co.kr/ticker?currency=all").text
	result = {}
	if jdat:
	    jdat = json.loads(jdat)
	else:
	    return None
	for ctype in ['btc', 'eth', 'etc', 'xrp', 'bch', 'ltc', 'qtum', 'bch','btg','iota']:
	    result[ctype.upper()] = int(jdat[ctype]['last'])
	return result

