import requests
import json
import pickle
import time

class Item:


    def __init__(self, id, name, members, sp, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity):
        #constructor
        #should only be called in setup, or when updates add new items to the game.
        #sets some variables, and sets up lists for variables that will be taken every time period for market history data
        self.id = id
        self.name = name
        self.members = members
        self.sp = sp
        self.buy_averages = [buy_average]
        self.buy_quantities = [buy_quantity]
        self.sell_averages = [sell_average]
        self.sell_quantities = [sell_quantity]
        self.overall_averages = [overall_average]
        self.overall_quantities = [overall_quantity]
        self.timestamps = [time.time()]
        if sell_average != 0 and buy_average !=0:
            self.margins = [buy_average - sell_average]
            self.rois = [(buy_average - sell_average) / sell_average]
        else:
            self.margins = [0]
            self.rois = [0]

    def update(self, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity):
        #called to add another history point for the market data of an item
        #appends price and volume data to lists, with a timestamp
        self.buy_averages.append(buy_average)
        self.buy_quantities.append(buy_quantity)
        self.sell_averages.append(sell_average)
        self.sell_quantities.append(sell_quantity)
        self.overall_averages.append(overall_average)
        self.overall_quantities.append(overall_quantity)
        self.timestamps.append(time.time())
        if sell_average != 0 and buy_average !=0:
            self.margins.append(buy_average - sell_average)
            self.rois.append((buy_average - sell_average) / sell_average)
        else:
            self.margins.append(0)
            self.rois.append(0)


    def cmargin(self):
        return self.margins[-1]
    def cbuy_quant(self):
        return self.buy_quantities[-1]
    def cbuy_price(self):
        return self.buy_averages[-1]
    def csell_quant(self):
        return self.sell_quantities[-1]
    def csell_price(self):
        return self.overall_averages[-1]
    def croi(self):
        return self.rois[-1]

    def getAverageMargin(self, time_amount):
        return self.getAverageBuyPrice(time_amount) - self.getAverageSellPrice(time_amount)

    def getAverageRoi(self, time_amount):
        sell_av =  self.getAverageSellPrice(time_amount)
        buy_av = self.getAverageBuyPrice(time_amount)
        if sell_av == 0 or buy_av == 0:
            return 0
        return (buy_av - sell_av) / sell_av

    def getAverageBuyPrice(self, time_amount):
        time_cutoff = time.time() - time_amount
        split_index = 0

        while(self.timestamps[split_index] < time_cutoff):
            split_index += 1


        buy_prices = self.buy_averages[split_index:]

        running_average = 0
        non_datafull_timestamps = 0

        for price in buy_prices:
            running_average += price
            if price == 0: non_datafull_timestamps += 1

        if(non_datafull_timestamps != len(buy_prices)):
            running_average /= (len(buy_prices)-non_datafull_timestamps)

        return running_average

    def getAverageSellPrice(self, time_amount):
        time_cutoff = time.time() - time_amount
        split_index = 0

        while(self.timestamps[split_index] < time_cutoff):
            split_index += 1


        sell_prices = self.sell_averages[split_index:]

        running_average = 0
        non_datafull_timestamps = 0

        for price in sell_prices:
            running_average += price
            if price == 0: non_datafull_timestamps += 1

        if(non_datafull_timestamps != len(sell_prices)):
            running_average /= (len(sell_prices)-non_datafull_timestamps)

        return running_average


    def last_10_buy_quant(self):
        running_sum = 0
        index = 0
        while index > -10:
            index -= 1
            running_sum += self.buy_quantities[index]
        return running_sum

    def last_10_sell_quant(self):
        running_sum = 0
        index = 0
        while index > -10:
            index -= 1
            running_sum += self.buy_quantities[index]
        return running_sum

    def __str__(self):
        temp = 'lmao'#ayy lmao
        CurrentROIitems_str = '{: <8} {: <28} with a margin of {: <10} a return on investment of {: <8} buy qty: {: <8} sell qty: {: <8} buy avg: {: <8} sell avg: {: <8}\n         Recent activity:\t      bought:{: <20} sold:{: <10}'
        CurrentROIitems_list = [self.overall_quantities, self.name, self.margins, self.rois, self.buy_quantities, self.sp, self.sell_quantities, self.buy_averages, self.sell_averages]
        for row in CurrentROIitems_list:
            return (CurrentROIitems_str.format(self.overall_quantities[-1], self.name, self.margins[-1], str(round(self.rois[-1], 3)), self.buy_quantities[-1], self.sell_quantities[-1], self.buy_averages[-1], self.sell_averages[-1], self.last_10_buy_quant(), self.last_10_sell_quant()).format(*row))







class MarketDatabase:
    def __init__(self, filename):
        #reads a preset database file and converts it into objects
        filehandler = open(filename, 'rb')
        self.filename = filename
        try:
            self.itemList = pickle.load(filehandler)
        except EOFError:
            self.itemList = []

    def writeToFile(self, filename):
        #writes a database file in pickle object notation
        filehandler = open(filename, 'wb')
        pickle.dump(self.itemList, filehandler)

    def updateItem(self, id, name, members, sp, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity):
        #Updated
        #added item buy price, sell price, ect. to lists that keep track of them over time
        #added some sort of timestamping functionality

        #if item is in itemlist, append data to lists
        found = False
        for item in self.itemList:
            if item.id == id:
                item.update(buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity)
                found = True

        #else if item is not in itemlist, add it to itemlist and initialize it
        if not found:
            item = Item(id, name, members, sp, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity)
            self.itemList.append(item)

        return "lmao"

    def getHighestMargins(self, listLen):
        assert(len(self.itemList) > listLen)
        topn = []
        for x in range(0,listLen):
            currentTop = None
            for item in self.itemList:
                if currentTop is None:
                    if item not in topn:
                        currentTop = item
                else:
                    if item.cmargin() > currentTop.cmargin() and item not in topn:
                        currentTop = item
            topn.append(currentTop)
        return topn

    def getHighestRois(self, listLen):
        assert(len(self.itemList) > listLen)
        topn = []
        for x in range(0,listLen):
            currentTop = None
            for item in self.itemList:
                if item.cbuy_price() > 50:
                    if currentTop is None:
                        if item not in topn:
                            currentTop = item
                    else:
                        if item.croi() > currentTop.croi() and item not in topn:
                            currentTop = item
            topn.append(currentTop)
        return topn

    def getHighestMargins_with_time(self, howmany, time_ago):
        assert (len(self.itemList) > howmany)
        topn = []
        for x in range(0, howmany):
            currentTop = None
            for item in self.itemList:
                if item.cbuy_price() > 50:
                    if currentTop is None:
                        if item not in topn:
                            currentTop = item
                    else:
                        if item.getAverageMargin(time_ago) > currentTop.getAverageMargin(time_ago) and item not in topn:
                            currentTop = item
            topn.append(currentTop)
        return topn

    def getHighestRois_with_time(self, howmany, time_ago):
        assert (len(self.itemList) > howmany)
        topn = []
        for x in range(0, howmany):
            currentTop = None
            for item in self.itemList:
                if item.cbuy_price() > 50:
                    if currentTop is None:
                        if item not in topn:
                            currentTop = item
                    else:
                        if item.getAverageRoi(time_ago) > currentTop.getAverageRoi(time_ago) and item not in topn:
                            currentTop = item
            topn.append(currentTop)
        return topn





    def __str__(self):
        ret = ""
        for item in self.itemList:
            ret += str(item) + "\n"
        return ret





market_data = requests.get('https://rsbuddy.com/exchange/summary.json')
market_data = json.loads(market_data.content)
database = MarketDatabase("osrs_data")

for item_data in market_data:
    item = market_data[item_data]
    database.updateItem(item['id'], item['name'], item['members'], item['sp'], int(item['buy_average']), item['buy_quantity'], int(item['sell_average']), item['sell_quantity'], item['overall_average'], item['overall_quantity'])

#highMarg = database.getHighestMargins(10)

tiem = 1000000

highMarg = database.getHighestRois_with_time(100, tiem)




print("Items currently with the return on investment")
for item in highMarg:
    print(str(item.name) + "  daily roi " + str(item.getAverageMargin(tiem)))

#print(database)
database.writeToFile("osrs_data")
print("done")


