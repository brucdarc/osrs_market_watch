import discord
import time
from Item import Item
from MarketDatabase import MarketDatabase
import math



TOKEN = ""
with open('token.txt', 'r') as file:
    TOKEN = file.read()



class MyClient(discord.Client):
    database = None
    async def on_ready(self): #triggers when bot starts up
        self.database = MarketDatabase("osrs_data")
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message): #triggers every time any message is sent in any channel
        #print('Message from {0.author}: {0.content}'.format(message))
        if message.content.startswith('$help'):
            ret = '''```A bot that returns custom queries from grand exchange data for old school runescape. 
Supports finding items with highest return on investment with conditions, and highest margin with conditions.

Commands

$topItem - finds the top items sorted based on either margin or return on investment that match your conditions

 Filters:

 - sort=(roi/margin/buy_price/sell_price) -choose which type of top 10 list you want

 - min_margin=(num) -only show items with at least this big of a margin

 - min_roi=(roi)	-only show items with at least this much of a return on investment

 - time=(number) (days/hours/minutes/seconds) - how far back in time do you want the bot to calculate margins.
            If this flag is not used, or time is 0, the program will only consider the latest market snapshot.

 - -v / verbose / -verbose  - display all the information about items in your query. 
 
 - number=(number of items) - how many items will the bot show you information for 
 
  - min_sell_quant=(num) - min sell quantity for the selected item period
 
 - max_sell_quant=(num) - max sell quantity for the selected item period
 
 - min_buy_quant=(num) - min buy quantity for the selected item period
 
 - max_buy_quant=(num) - max buy quantity for the selected item period
 
 - min_total_quant=(num) - min total quantity for the selected item period
 
 - max_total_quant=(num) - max total quantity for the selected item period
 
 - min_sell_price=(num) - min sell price for the selected item period
 
 - max_sell_price=(num) - max sell price for the selected item period
 
 - min_buy_price=(num) - min buy price for the selected item period
 
 - max_buy_price=(num) - max buy price for the selected item period
 
 - members=(True/False) - is the item only usable by members```'''
            ret2 = '''```$searchItem <\item name>- Displays information about a particular item

$help - Shows some useful information

More sort filters and features comming soon!



Example Queries

$topItem sort=roi min_margin=500

$topItem sort=margin min_roi=0.10

$topItem sort=margin min_roi=0.05 time=5 hours

$searchItem Logs ```'''


            await message.channel.send(str(ret))
            await message.channel.send(str(ret2))

        if message.content.startswith('$topItem'):
            await self.handleQuery(message)


        if message.content.startswith('$searchItem'):
            query = message.content[12:]
            print(query)
            items = self.database.itemList

            found = False

            for item in items:
                if item.name.lower() == query.lower():
                    found = True
                    await message.channel.send("https://www.ge-tracker.com/item/" + item.name.replace(' ', '-').lower().replace('(', '-').replace(')', ''))
                    await message.channel.send("```" + str(item) + "```")
            if not found:
                await message.channel.send("Could not find item. Check spelling and capitalization.")


    async def handleQuery(self, message):
        args = message.content.split(" ")

        sort, time, min_marg, min_roi, verbose, number_of_items_to_retrieve, max_marg, max_roi, min_sell_quant, max_sell_quant, \
               min_buy_quant, max_buy_quant, min_total_quant, max_total_quant, \
               min_sell_price, max_sell_price, min_buy_price, max_buy_price, members = await self.parseArgs(args, message)

        if number_of_items_to_retrieve > 50:
            await message.channel.send("Cannot complete request, maximum query size is 50 items.")
            raise(Exception())

        topItems, values = self.database.getHighestAttr_with_time(number_of_items_to_retrieve, time_ago=time, sortby=sort, min_margin=min_marg, min_roi=min_roi,
                                                                  max_margin=max_marg, max_roi=max_roi, min_sell_quantity=min_sell_quant, max_sell_quantity=max_sell_quant,
                                                                  min_buy_quantity=min_buy_quant, max_buy_quantity=max_buy_quant, min_total_quantity=min_total_quant,
                                                                  max_total_quantity=max_total_quant, min_buy_price=min_buy_price, max_buy_price=max_buy_price,
                                                                  min_sell_price=min_sell_price, max_sell_price=max_sell_price, is_members=members)
        # print(topItems)
        bot_response = ""
        for x in range(0, len(topItems)):
            item = topItems[x]
            url = "https://www.ge-tracker.com/item/" + item.name.replace(' ', '-').lower().replace('(', '-').replace(
                ')', '').replace('\'', '-').replace('--', '-')

            # url_image = "https://storage.ge-tracker.com/icons/" + str(item.id) + ".png"
            # make response string print the attribute the user was asking to sort by
            test_bot_response = bot_response
            if not verbose:
                test_bot_response += "#" + str(x + 1) + " " + str(item.name) + " - " + sort + " : "
                test_bot_response += str(round(values[x], 2)) + "  "
                test_bot_response += url + "\n"
            else:
                test_bot_response += "#" + str(x + 1) + "```" + item.uberStr(time) + "```"

            #make sure we dont go over discord character limit per message. If a message would be too big after adding an item,
            #put that item into the next message instead
            if len(test_bot_response) > 2000:
                await message.channel.send(bot_response)
                added_len = len(test_bot_response) - len(bot_response)

                bot_response = test_bot_response[-added_len:]

            else: bot_response = test_bot_response


        if len(topItems) == 0:
            bot_response = "Error: No item data found for selected time period. Please try a longer timer period. Market snapshots are taken every 10 minutes. If you think this is a bug, please contact my developer."
        elif bot_response != "":
            await message.channel.send(bot_response)

        await message.channel.send("Found " + str(len(topItems)) + " items matching your query")


    async def parseArgs(self, args, message):
        sort = "roi"
        time = 0
        min_marg = 0
        min_roi = 0
        max_marg = 0
        max_roi = 0
        verbose = False
        number = 10
        min_sell_quant = 0
        max_sell_quant = 0
        min_buy_quant = 0
        max_buy_quant = 0
        min_total_quant = 0
        max_total_quant = 0
        min_sell_price = 0
        max_sell_price = 0
        min_buy_price = 0
        max_buy_price = 0
        members = True



        for x in range(0, len(args)):
            arg = args[x]
            if arg.startswith("sort="):
                sort = arg[5:]
            if arg.startswith("min_margin="):
                min_marg = int(arg[11:])
            if arg.startswith("min_roi="):
                min_roi = float(arg[8:])
            if arg.startswith("max_margin="):
                max_marg = int(arg[11:])
            if arg.startswith("max_roi="):
                max_roi = float(arg[8:])

            if arg.startswith("min_sell_quant="):
                min_sell_quant = float(arg[15:])

            if arg.startswith("max_sell_quant="):
                max_sell_quant = float(arg[15:])

            if arg.startswith("min_buy_quant="):
                min_buy_quant = float(arg[14:])

            if arg.startswith("max_buy_quant="):
                max_buy_quant = float(arg[14:])

            if arg.startswith("min_total_quant="):
                min_total_quant = float(arg[16:])

            if arg.startswith("max_total_quant="):
                max_total_quant = float(arg[16:])



            if arg.startswith("min_sell_price="):
                min_sell_price = float(arg[15:])

            if arg.startswith("max_sell_price="):
                max_sell_price = float(arg[15:])

            if arg.startswith("min_buy_price="):
                min_buy_price = float(arg[14:])

            if arg.startswith("max_buy_price="):
                max_buy_price = float(arg[14:])

            if arg.startswith("members="):
                if arg[8:].lower() == "true":
                    members = True




            if arg.startswith("-v") or arg.startswith("verbose") or arg.startswith("-verbose"):
                verbose = True
            if arg.startswith("number="):
                number = int(arg[7:])


            if arg.startswith("time="):
                time = int(arg[5:])
                if len(args) <= x + 1:
                    await message.channel.send("Please provide a valid time unit. (days/hours/minutes/seconds)")
                    raise Exception('Please provide a valid time unit. (days/hours/minutes)')
                time_unit = args[x + 1]
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
                    raise Exception('Please provide a valid time unit. (days/hours/minutes)')
        return sort, time, min_marg, min_roi, verbose, number, max_marg, max_roi, min_sell_quant, max_sell_quant, \
               min_buy_quant, max_buy_quant, min_total_quant, max_total_quant, \
               min_sell_price, max_sell_price, min_buy_price, max_buy_price, members




client = MyClient()
client.run(TOKEN)