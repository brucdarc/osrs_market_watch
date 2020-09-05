import discord
import time
from Item import Item
from MarketDatabase import MarketDatabase
import math

TOKEN = 'NjQ0NDAyNTMyNzU1NzAxNzYx.XczgoA.YZb4CYWv4-pOtKq8rVNfy77yLDM'


class MyClient(discord.Client):
    database = None
    async def on_ready(self): #triggers when bot starts up
        self.database = MarketDatabase("osrs_data")
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message): #triggers every time any message is sent in any channel
        #print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith('$help'):
            print("test")


        if message.content.startswith('$topItem'):
            args = message.content.split(" ")
            sort = "roi"
            time = 0

            for x in range(0, len(args)):
                arg = args[x]
                if arg.startswith("sort="):
                    sort = arg[5:]
                if arg.startswith("time="):
                    time = int(arg[5:])
                    if len(args) <= x+1:
                        await message.channel.send("Please provide a valid time unit. (days/hours/minutes/seconds)")
                        return
                    time_unit = args[x+1]
                    if time_unit.startswith('day'):
                        time *= 86400
                    elif time_unit.startswith('hour'):
                        time *= 3600
                    elif time_unit.startswith('minute'):
                        time *= 60
                    elif time_unit.startswith('second'):
                        time = time
                    else:
                        await message.channel.send("Please provide a valid time unit. (days/hours/minutes)")
                        return




            topItems = self.database.getHighestAttr_with_time(25, time_ago=time, sortby=sort)
            bot_response = ""
            for item in topItems:
                url = "https://www.ge-tracker.com/item/" + item.name.replace(' ', '-').lower().replace('(', '-').replace(')', '')
                #TODO make response string print the attribute the user was asking to sort by, and care about if they specifed a timer period, or just the last snapshot
                bot_response += str(item.name) + " " + url + "\n"

            if len(topItems) == 0:
                bot_response = "Error: No item data found for selected time period. Please try a longer timer period. Market snapshots are taken every 10 minutes. If you think this is a bug, please contact my developer."
            if len(bot_response) < 2000:
                await message.channel.send(bot_response)
            else:
                messages = math.ceil(len(bot_response)/2000)
                cutoff = 0
                for x in range(0,messages):
                    if(cutoff+2000<len(bot_response)):
                        await message.channel.send(bot_response[cutoff:cutoff+2000])
                    else:
                        await message.channel.send(bot_response[cutoff:])
                    cutoff += 2000

        #supported sort:
        #roi
        #margin
        #more to come





client = MyClient()
client.run(TOKEN)