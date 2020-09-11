# WFMarket-Price-Checker
Tool that scans the warframe.market API to retrieve the platinum price (lowest to highest) of valid (items that are listed on warframe.martket) items from listings by users that are both selling and have set their status to in-game

User inputs the desired search item - if the item is listed on waframe.market the relevant data (username of the player selling, the quantity, the price of the item (the mod rank for 'mods') and the URL for the players profile) is sorted (in order of lowest to highest price) and is printed.

Otherwise an error is reported and the user can search again after a short time.
