

import time
import numpy


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
        #Todo make this take percentile not just average, bad for flips
        time_cutoff = time.time() - time_amount
        split_index = 0
        if len(self.timestamps) == 0:
            return 0
        if(self.timestamps[-1] < time_cutoff):
            return 0
        while(self.timestamps[split_index] < time_cutoff):

            if self.timestamps[split_index] < time_cutoff:
                split_index += 1


        buy_prices = self.buy_averages[split_index:]

        running_average = 0
        non_datafull_timestamps = 0
        meaningful_datapoints = []

        for price in buy_prices:
            running_average += price
            if price == 0: non_datafull_timestamps += 1
            else: meaningful_datapoints.append(price)


        if(non_datafull_timestamps != len(buy_prices)):
            running_average /= (len(buy_prices)-non_datafull_timestamps)

        percentile = 90
        result = 0
        if len(meaningful_datapoints) != 0:
            result = numpy.percentile(meaningful_datapoints, percentile)

        return result



    def getAverageSellPrice(self, time_amount):
        #Todo make this take percentile not just average, bad for flips
        time_cutoff = time.time() - time_amount
        split_index = 0
        if len(self.timestamps) == 0:
            return 0
        if(self.timestamps[-1] < time_cutoff):
            return 0
        while(self.timestamps[split_index] < time_cutoff):
            if self.timestamps[split_index] < time_cutoff:
                split_index += 1


        sell_prices = self.sell_averages[split_index:]

        running_average = 0
        meaningful_datapoints = []
        non_datafull_timestamps = 0

        for price in sell_prices:
            running_average += price
            if price == 0: non_datafull_timestamps += 1
            else: meaningful_datapoints.append(price)

        if(non_datafull_timestamps != len(sell_prices)):
            running_average /= (len(sell_prices)-non_datafull_timestamps)

        percentile = 10
        result = 0
        if len(meaningful_datapoints) != 0:
            result = numpy.percentile(meaningful_datapoints, percentile)

        return result


    def last_10_buy_quant(self):
        if (len(self.buy_quantities) < 10): return ""
        running_sum = 0
        index = 0
        while index > -10:
            index -= 1
            running_sum += self.buy_quantities[index]
        return running_sum

    def last_10_sell_quant(self):
        if(len(self.buy_quantities) < 10): return ""
        running_sum = 0
        index = 0
        while index > -10:
            index -= 1
            running_sum += self.buy_quantities[index]
        return running_sum

    def __str__(self):
        temp = 'lmao'#ayy lmao
        CurrentROIitems_str = '{: <18} most recent margin: {: <7} most recent ROI: {: <17} \nbuy qty: {: <8} sell qty: {: <8} buy avg: {: <12} sell avg: {: <12}\nRecent activity:\t      bought:{: <20} sold:{: <10}\nOver the last 24 hours: \t average margin: {: <11} average ROI: {: <21} \naverage buy price: {: <17} average sell price: {}\n'
        CurrentROIitems_list = [self.name, self.margins, self.rois, self.buy_quantities, self.sp, self.sell_quantities, self.buy_averages, self.sell_averages]
        for row in CurrentROIitems_list:
            return (CurrentROIitems_str.format(self.name, self.margins[-1], str(round(self.rois[-1], 3)), self.buy_quantities[-1], self.sell_quantities[-1], self.buy_averages[-1], self.sell_averages[-1], self.last_10_buy_quant(), self.last_10_sell_quant(), str(round(self.getAverageMargin(86400), 3)), str(round(self.getAverageRoi(86400), 3)), str(round(self.getAverageBuyPrice(86400), 3)), str(round(self.getAverageSellPrice(86400), 3))).format(*row))


    def __repr__(self): return self.__str__()