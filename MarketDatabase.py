
import pickle
import time
import numpy

class MarketDatabase:
    def __init__(self, filename):
        # reads a preset database file and converts it into objects
        filehandler = open(filename, 'rb')
        self.filename = filename
        try:
            self.itemList = pickle.load(filehandler)
        except EOFError:
            self.itemList = []

    def writeToFile(self, filename):
        # writes a database file in pickle object notation
        filehandler = open(filename, 'wb')
        pickle.dump(self.itemList, filehandler)

    def updateItem(self, id, name, members, sp, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity):
        # Updated
        # added item buy price, sell price, ect. to lists that keep track of them over time
        # added some sort of timestamping functionality

        # if item is in itemlist, append data to lists
        found = False
        for item in self.itemList:
            if item.id == id:
                item.update(buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity)
                found = True

        # else if item is not in itemlist, add it to itemlist and initialize it
        if not found:
            item = Item(id, name, members, sp, buy_average, buy_quantity, sell_average, sell_quantity, overall_average, overall_quantity)
            self.itemList.append(item)

        return "lmao"

    def getHighestMargins(self, listLen):
        assert(len(self.itemList) > listLen)
        topn = []
        for x in range(0 ,listLen):
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
        for x in range(0 ,listLen):
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

    def getHighestRois_with_time(self, number_to_retrieve, time_ago, min_margin=0, max_margin=0, min_roi=0,
                                 max_roi=0, min_dailY_quantity=0, max_daily_quantity=0, is_members=False, min_price=0, max_price=0):



        topn = []
        for x in range(0, number_to_retrieve):
            currentTop = None
            for item in self.itemList:
                search_conditions = item.getAverageMargin(time_ago) > min_margin
                if item.cbuy_price() > 50:
                    if currentTop is None:
                        if item not in topn and search_conditions:
                            currentTop = item
                    else:
                        if item.getAverageRoi(time_ago) > currentTop.getAverageRoi \
                                (time_ago) and item not in topn and search_conditions:
                            currentTop = item
            if currentTop is not None:
                topn.append(currentTop)
        return topn





    def __str__(self):
        ret = ""
        for item in self.itemList:
            ret += str(item) + "\n"
        return ret


