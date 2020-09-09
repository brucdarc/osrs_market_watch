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
            ret = "```Commands \n\n$topItem - finds the top items sorted based on either margin or return on investment that match your conditions\n\n\tFilters\n\n\t - sort=<roi/margin> -choose which type of top 10 list you want\n\n\t - min_margin=<num> -only show items with at least this big of a margin\n\n\t - min_roi=<roi> -only show items with at least this much of a return on investment\n\n\t - time=(number) (days/hours/minutes/seconds) - how far back in time do you want the bot to calculate margins. If this flag is not used, or time is 0, the program will only consider the latest market snapshot\n\n$searchItem <item name>- displays information about a particular item\n\nMore sort filters and features comming soon!\n```"
            await message.channel.send(str(ret))

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

        sort, time, min_marg, min_roi = await self.parseArgs(args, message)

        topItems, values = self.database.getHighestAttr_with_time(20, time_ago=time, sortby=sort, min_margin=min_marg, min_roi=min_roi)
        # print(topItems)
        bot_response = ""
        for x in range(0, len(topItems)):
            item = topItems[x]
            url = "https://www.ge-tracker.com/item/" + item.name.replace(' ', '-').lower().replace('(', '-').replace(
                ')', '').replace('\'', '-').replace('--', '-')

            # url_image = "https://storage.ge-tracker.com/icons/" + str(item.id) + ".png"
            # make response string print the attribute the user was asking to sort by
            bot_response += "#" + str(x + 1) + " " + str(item.name) + " - " + sort + " : "
            bot_response += str(round(values[x], 2)) + "  "
            bot_response += url + "\n"

        if len(topItems) == 0:
            bot_response = "Error: No item data found for selected time period. Please try a longer timer period. Market snapshots are taken every 10 minutes. If you think this is a bug, please contact my developer."
        if len(bot_response) < 1994:
            await message.channel.send(bot_response)
        else:
            messages = math.ceil(len(bot_response) / 2000)
            cutoff = 0
            for x in range(0, messages):
                if (cutoff + 2000 < len(bot_response)):
                    await message.channel.send(bot_response[cutoff:cutoff + 2000])
                else:
                    await message.channel.send(bot_response[cutoff:])
                cutoff += 2000

    async def parseArgs(self, args, message):
        sort = "roi"
        time = 0
        min_marg = 0
        min_roi = 0

        for x in range(0, len(args)):
            arg = args[x]
            if arg.startswith("sort="):
                sort = arg[5:]
            if arg.startswith("min_margin="):
                min_marg = int(arg[11:])
            if arg.startswith("min_roi="):
                min_roi = float(arg[8:])

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
        return sort, time, min_marg, min_roi




client = MyClient()
client.run(TOKEN)