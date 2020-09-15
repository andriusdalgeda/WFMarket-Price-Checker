import requests
import json
import string
import time

#   Search the warframe.market API to find the listings of valid (and tradable) items on warframe.market, returning the platinum price of valid (both selling and ingame) listings
#   Also displaying the mod rank for applicable items on warframe.market

def WFMarket_search_ingame_seller():
    while True:
        try:
            
            # User input
            print('Search for an item on warframe.market: ')
            search = input()
            item_url = 'https://warframe.market/items/' + search.replace(' ', '_')

            # Prints the search item for QoL
            print('Searching for listings of ' + string.capwords(search) + '... (' + item_url + ')','\n')

            # Start time for search
            start = time.time()

            # Requests response from online_URL and parses json data
            online_URL = 'https://api.warframe.market/v1/items/' + search.replace(' ', '_') + '/orders'
            online_request = requests.get(online_URL)
            online_json = online_request.json()

            # Sorts all values in json response from lowest to highest 'platinum' for easy interpretation within the console
            for val in sorted(online_json["payload"]["orders"], key=lambda x:int(x['platinum'])):

                # Only prints the listings from users that are ingame and are selling the searched item
                if val["user"]["status"] == "ingame" and val["order_type"] == "sell":
                    
                    # Common values within both print statements
                    username = val["user"]["ingame_name"]
                    plat_price = int(val["platinum"])
                    quantity = int(val["quantity"])
                    profile_URL = 'https://warframe.market/profile/' + username
    
                    # If 'mod_rank' is present in the online_json the item is assumed to be a 'mod'
                    if "mod_rank" in val:
                        rank = int(val["mod_rank"])
                        print(username,'is selling ',str(quantity),'at rank', str(rank),'for',str(plat_price) ,'Platinum each.',''*5,'(' + profile_URL + ')')
                        
                    # If an item is not a mod, its assumed to be a regular 'item'
                    else:
                        print(username,'is selling',str(quantity),'for',str(plat_price),'Platinum each.',''*5,'(' + profile_URL + ')')

            # Prints time taken to complete request
            print('\n' + 'The request took', time.time()-start,'seconds','\n')

            # Waits for 334ms before taking another request (limitation of 3 requests/second)
            time.sleep(334/1000)
            WFMarket_search_ingame_seller()

        # If the item is not a valid listing on warframe.market a key error is returned
        except KeyError:
            print("Invalid Item - Please check the spelling or enter a valid (and tradable) Warframe item ('Frost Prime Systems', 'Axi L4 Intact', 'Dead Eye')")
            time.sleep(334/1000)
            WFMarket_search_ingame_seller()
            
        # Error checking for whether the API is down
        except json.JSONDecodeError:
            print('The warframe.market API is currently down, please try again later.')
            break
        
WFMarket_search_ingame_seller()