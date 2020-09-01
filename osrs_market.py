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

for item_data in market_data:
    item = market_data[item_data]
    database.updateItem(item['id'], item['name'], item['members'], item['sp'], int(item['buy_average']), item['buy_quantity'], int(item['sell_average']), item['sell_quantity'], item['overall_average'], item['overall_quantity'])

#highMarg = database.getHighestMargins(10)

tiem = 86400

#highMarg = database.getHighestRois_with_time(100, tiem, 5000)
highMarg = []



print("Items currently with the return on investment")
for item in highMarg:
    print(item)

print("\n\n\nspecific test items:\n\n\n")

for item in database.itemList:
    if 'book page set' in item.name:
        print(item)

#print(database)
database.writeToFile("osrs_data")
print("done")


