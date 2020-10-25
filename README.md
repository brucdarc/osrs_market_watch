# osrs_market_watch

A bot that returns custom queries from grand exchange data for old school runescape. 
Supports finding items with highest return on investment with conditions, and highest margin with conditions.

Commands

`$topItem` - finds the top items sorted based on either margin or return on investment that match your conditions

 Filters:

 - `sort=(roi/margin)` -choose which type of top 10 list you want

 - `min_margin=(num)` -only show items with at least this big of a margin

 - `min_roi=(roi)`	-only show items with at least this much of a return on investment

 - `time=(number) (days/hours/minutes/seconds)` - how far back in time do you want the bot to calculate margins. If this flag is not used, or time is 0, the program will only consider the latest market snapshot 

 - `-v` / `verbose` / `-verbose`  - display all the information about items in your query. 
 
 - `number=(number of items)` - how many items will the bot show you information for 
 
 - `min_sell_quant=(num)` - min sell quantity for the selected item period
 
 - `max_sell_quant=(num)` - max sell quantity for the selected item period
 
 - `min_buy_quant=(num)` - min buy quantity for the selected item period
 
 - `max_buy_quant=(num)` - max buy quantity for the selected item period
 
 - `min_total_quant=(num)` - min total quantity for the selected item period
 
 - `max_total_quant=(num)` - max total quantity for the selected item period
 
 - `min_sell_price=(num)` - min sell price for the selected item period
 
 - `max_sell_price=(num)` - max sell price for the selected item period
 
 - `min_buy_price=(num)` - min buy price for the selected item period
 
 - `max_buy_price=(num)` - max buy price for the selected item period
 
 - `members=(True/False)` - is the item only usable by members
  
  

`$searchItem <\item name>`- Displays information about a particular item

`$help` - Shows some useful information

More sort filters and features comming soon!



Example Queries

`$topItem sort=roi min_margin=500`

`$topItem sort=margin min_roi=0.10`

`$topItem sort=margin min_roi=0.05 time=5 hours`

`$searchItem Logs`
