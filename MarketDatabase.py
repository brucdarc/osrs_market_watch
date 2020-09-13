
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



    def getHighestAttr_with_time(self, number_to_retrieve, time_ago=0, min_margin=0, sortby="roi", max_margin=0, min_roi=0,
                                 max_roi=0, min_dailY_quantity=0, max_daily_quantity=0, is_members=False, min_sell_price=0, max_sell_price=0,
                                 min_buy_price=0, max_buy_price=0):



        #run through items, grab all of them that meet my search criteria
        #create tuple pairs of the items, and the sort condition i want to sort them by
        #sort the list of (item, sort_var) based on the variable i want to sort by
        tuple_item_list = []
        #do boolean checks for all the user inputed conditions, and only consider the items that meet those conditions for the final return list
        print("start " + str(time.time()))
        for item in self.itemList:

            #check all the conditions for each item, to see if it makes it into our list.
            #average methods just return the last known value if time is 0
            sell_price = item.getAverageSellPrice(time_ago)
            buy_price = item.getAverageBuyPrice(time_ago)
            margin = buy_price - sell_price
            roi = 0
            if sell_price != 0:
                roi = (buy_price - sell_price) / sell_price

            #mins
            search_conditions = margin > min_margin
            search_conditions = search_conditions and roi > min_roi
            search_conditions = search_conditions and sell_price > min_sell_price
            search_conditions = search_conditions and buy_price > min_buy_price
            #other
            search_conditions = search_conditions and (item.members == is_members)
            #maxes
            search_conditions = (search_conditions and margin > max_margin) or max_margin == 0
            search_conditions = (search_conditions and roi < max_roi) or max_roi == 0
            search_conditions = (search_conditions and sell_price > max_sell_price) or max_sell_price == 0
            search_conditions = (search_conditions and buy_price > max_buy_price) or max_buy_price == 0

            if search_conditions:
                if sortby == "roi":
                    tuple_paired_item = (item, roi)
                elif sortby == "margin":
                    tuple_paired_item = (item, margin)
                elif sortby == "sell_price":
                    tuple_paired_item = (item, sell_price)
                elif sortby == "buy_price":
                    tuple_paired_item = (item, buy_price)
                else:
                    raise Exception('attribute to sort by is not supported')
                tuple_item_list.append(tuple_paired_item)

        print("finish " + str(time.time()))
        print(sortby)

        #create tuple pairs of the item, and the user defined search attribute. Sort the tuple list, then take the top n, where n is how many the user requested
        #currently supports sort parameters roi, and margin
        #TODO: allow user to ignore time, and use getRoi and getMargin to get those attributes for only the latest market snapshot

        sorted_tuples = sorted(tuple_item_list, key=lambda x: x[-1])
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


