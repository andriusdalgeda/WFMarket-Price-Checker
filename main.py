import requests
import json
import string
import time

#   Search the warframe.market API to find the listings of valid (and tradable) items on warframe.market, returning the platinum price of valid (both selling and ingame) listings
#   Also displaying the mod rank for applicable items on warframe.market

def WFMarket_search_ingame_seller():
    while True:
        try:
            print('Search for an item on warframe.market: ')
            search = input()
            print('Searching for listings of ' + string.capwords(search) + '....' )

            online_URL = 'https://api.warframe.market/v1/items/' + search.replace(' ', '_') + '/orders'
            online_request = requests.get(online_URL)
            online_json = online_request.json()

            # Sorts all values in json response from lowest to highest 'platinum'
            for val in sorted(online_json["payload"]["orders"], key=lambda x:int(x['platinum'])):

                # Ignores 'offline' and 'online' response to ["status"] and also ignores "buy" orders and only prints "sell" orders (users that are selling and are currently ingame)
                if val["user"]["status"] == "ingame" and val["order_type"] == "sell":
                    
                    username = val["user"]["ingame_name"]
                    plat_price = int(val["platinum"])
                    quantity = int(val["quantity"])
                    profile_URL = 'https://warframe.market/profile/' + username

                    # If 'mod_rank' is present in the .json response, the item is assumed to be a mod
                    if "mod_rank" in val:
                        rank = int(val["mod_rank"])
                        print(username, 'is selling ',  str(quantity), ' at rank ', str(rank), ' for ',  str(plat_price) , ' Platinum each.',  ' '*30,  profile_URL) 

                    # If an item is not a mod, it must be a regular 'item'
                    else:
                        print(username, ' is selling ', str(quantity), ' for ', str(plat_price), ' Platinum each.',  ' '*30, profile_URL)

            # Waits for 334ms before taking another request (TOU limitation of 3 requests per second)
            time.sleep(334/1000)
            WFMarket_search_ingame_seller()

        # Key error, if item is not a valid listing on warframe.market error is returned
        except KeyError:
            print("Invalid Item - Please check the spelling or enter a valid (and tradable) Warframe item ('Frost Prime Systems', 'Axi L1 Intact', 'Dead Eye')")
            time.sleep(334/1000)
            WFMarket_search_ingame_seller()

WFMarket_search_ingame_seller()

