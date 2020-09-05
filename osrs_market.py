import requests
import json
import pickle
import time
import numpy
from Item import Item
from MarketDatabase import MarketDatabase



market_data = requests.get('https://rsbuddy.com/exchange/summary.json')
market_data = json.loads(market_data.content.decode('utf8'))
database = MarketDatabase("osrs_data")


tiem = 86400

highMarg = database.getHighestAttr_with_time(10, tiem, 5000)

#currently with the return on investment")
for item in highMarg:
    print(item)

print("\n\n\nspecific test items:\n\n\n")


for item in database.itemList:
    if 'book page set' in item.name:
        print(item)


print("Items")

print("done")


