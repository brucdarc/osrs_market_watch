import requests
import json
import pickle
import time
import numpy
from Item import Item
from MarketDatabase import MarketDatabase

snapshot_number = 0

while(True):
    try:
        market_data = requests.get('https://rsbuddy.com/exchange/summary.json')
        market_data = json.loads(market_data.content.decode('utf8'))
        database = MarketDatabase("osrs_data")

        for item_data in market_data:
            item = market_data[item_data]
            database.updateItem(item['id'], item['name'], item['members'], item['sp'], int(item['buy_average']), item['buy_quantity'], int(item['sell_average']), item['sell_quantity'], item['overall_average'], item['overall_quantity'])
        database.writeToFile("osrs_data")
        snapshot_number += 1
        print("done with market snapshot " + str(snapshot_number) + " at time " + str(time.time()))
    except Exception:
        print("connection failed, trying again in 10 minutes")

    time.sleep(60*10)