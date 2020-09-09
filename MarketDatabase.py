
import pickle
import time
import numpy
from Item import Item
#import sorted


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



    def getHighestAttr_with_time(self, number_to_retrieve, time_ago=0, min_margin=0, sortby="roi", max_margin=0, min_roi=0,
                                 max_roi=0, min_dailY_quantity=0, max_daily_quantity=0, is_members=False, min_price=0, max_price=0):



        #run through items, grab all of them that meet my search criteria
        #create tuple pairs of the items, and the sort condition i want to sort them by
        #sort the list of (item, sort_var) based on the variable i want to sort by

        valid_item_canditates = []
        #do boolean checks for all the user inputed conditions, and only consider the items that meet those conditions for the final return list
        for item in self.itemList:
            if time_ago != 0:
                search_conditions = item.getAverageMargin(time_ago) > min_margin
                search_conditions = search_conditions and item.getAverageRoi(time_ago) > min_roi
            else:
                search_conditions = item.cmargin() > min_margin
            if search_conditions:
                valid_item_canditates.append(item)

        tuple_item_list = []

        print(sortby)

        #create tuple pairs of the item, and the user defined search attribute. Sort the tuple list, then take the top n, where n is how many the user requested
        #currently supports sort parameters roi, and margin
        #TODO: allow user to ignore time, and use getRoi and getMargin to get those attributes for only the latest market snapshot
        for item in valid_item_canditates:
            if time_ago != 0:
                if sortby=="roi":
                    tuple_paired_item = (item, item.getAverageRoi(time_ago))
                elif sortby=="margin":
                    tuple_paired_item = (item, item.getAverageMargin(time_ago))
                    #print(item.getAverageMargin(time_ago))
                else:
                    raise Exception('attribute to sort by is not supported')
            else:
                if sortby=="roi":
                    tuple_paired_item = (item, item.croi())
                elif sortby=="margin":
                    tuple_paired_item = (item, item.cmargin())
                else:
                    raise Exception('attribute to sort by is not supported')

            tuple_item_list.append(tuple_paired_item)

        #print(tuple_item_list)

        sorted_tuples = sorted(tuple_item_list, key=lambda x: x[-1])

        #print(sorted_tuples)
        sorted_tuples.reverse()

        topn = [tup[0] for tup in sorted_tuples]
        attrs = [tup[1] for tup in sorted_tuples]

        if len(topn) > number_to_retrieve:
            return topn[:number_to_retrieve], attrs[:number_to_retrieve]
        else: return topn, attrs


    def __str__(self):
        ret = ""
        for item in self.itemList:
            ret += str(item) + "\n"
        return ret


