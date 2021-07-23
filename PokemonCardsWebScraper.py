import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver

results = []

# Red Nails 2
urls = ['https://www.rednails2.com/gaming/pokemon/pokemon-sword-and-shield-chilling-reign-booster-box/'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.find('p', {'class':'price'})
    price = list(price.find('span', {'class':'woocommerce-Price-amount'}).children)
    length = len(price)
    price = price[length - 1] # Price is last one
    stock = soup.find('button',{'name':'add-to-cart'})
    if (str(stock) == 'None'):
        stock = "Sold Out"
    else:
        stock = list(stock.stripped_strings)[0]    
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# Kanzen Games, Skaf Express
urls = ['https://kanzengames.com/collections/cr-sealed-product/products/copy-of-pokemon-chilling-reign-booster-box-pre-order-june-18th-2021',
#'https://www.skafexpress.ca/products/pokemon-swsh6-chilling-reign-elite-trainer-box-blue'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.find('meta', property='og:price:amount')
    if (str(price) == 'None'): # Skaf Express is different
        price = soup.find('meta', property='product:price:amount')
    price = price["content"]
    stock = list(list(soup.find('button',{'name':'add'}).children)[1].stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# Wizard's Tower / Kanata Tcg
urls = ['https://www.kanatacg.com/catalog/pokemon_sealed_products-pokemon_booster_packs/chilling_reign_booster_box_36_packs/499031'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Sometimes they use spans / classes, othertimes no just straight up tables
    price = soup.find('span',{'class':'price'})
    stock = soup.find('span',{'class':'qty'})
    if (str(price) == 'None' or str(stock) == 'None'):
        # Only way to find the right price since website is weird with prices
        data = list(list(soup.find(attrs={'class':'invisible-table cell-center'}).children)[3].children) # first is head, second is body, but \n every other item
        data = list(data[1].children) # Get all the row data
        length = len(data)
        price = list(data[length - 6].stripped_strings)[0]
        stock = list(data[length - 4].stripped_strings)[0]
    else:
        price = list(price.stripped_strings)[0]
        stock = list(stock.stripped_strings)[0] + " in stock"
    
    title = list(soup.find('title').stripped_strings)[0].split('-')[0]
    data = [price, stock, title]
    results.append(data)



# Magic Stronghold
#urls = ['https://www.magicstronghold.com/store/category/Pokemon%20Sealed%20Product/item/239517/Sword_&_Shield:_Chilling_Reign_Booster_Box',
#'https://www.magicstronghold.com/store/category/Pokemon%20Sealed%20Product/item/110403/Sun_&_Moon_-_Crimson_Invasion_Booster_Box'
#]
#for url in urls:
#    response = requests.get(url)
#    soup = BeautifulSoup(response.text, "html.parser")

    #For whatever reason this doesn't load, even with chromedriver or headers
 #   price = soup.find('span',{'class':'price'})
#    stock = soup.find('div',{'class':'stock'})
#    title = soup.find(id='fullStoreName') 
#    data = [price, stock, title]
#    print(data)
#    results.append(data)


# Game Shack
urls = ['https://gameshack.ca/pokemon-ss5-chilling-reign-booster-box.html'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find(attrs={'class':'add-to-cart-wrapper'}) # Only way to find the right price since website is weird with prices
    price = list(data.find(attrs={'class':'price'}).stripped_strings)[0]
    stock = list(list(data.find(attrs={'class':'availability'}).children)[1].stripped_strings)[0]
    title = list(list(soup.find(attrs={'class':'logo'}).children)[0].stripped_strings)[0]
    data = [price, stock, title]
    results.append(data)


# The League's Den
urls = ['https://www.theleaguesden.com/product/pokemon-tcg-sword-shield-chilling-reign-booster-box-sealed-36-packs-/68'
]
for url in urls:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Surpess bluetooth adapter error since my pc doesn't have bluetooth
    browser = webdriver.Chrome(options=options) # Need to use chromium webdriver since these websites load stock dynamically

    data = 'None'
    while(str(data) == 'None'): # Occasionally returns none, so loop until it doesn't
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        data = soup.find('script', type='application/ld+json')

    data = json.loads(list(data.children)[0])['mainEntity']['offers']

    price = str(data['price'])
    stockList = data['availability'].split('/')
    length = len(stockList)
    stock = stockList[length - 1]
    if (str(stock) == 'InStock'):
        stock = "In Stock"
    elif (str(stock) == "OutOfStock"):
        stock = "Sold Out"
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)
    browser.close()



# New Realm Games, Cardboard Memories, Face to Face Games
urls = ['https://newrealmgames.com/collections/pokemon-sealed-product/products/pokemon-chilling-reign-booster-box-pre-order-june-2021',
'https://www.cardboardmemories.ca/products/pokemon-sword-and-shield-chilling-reign-booster-box?',
'https://www.facetofacegames.com/pokemon-tcg-sword-shield-chilling-reign-booster-box/'
]
for url in urls:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Surpess bluetooth adapter error since my pc doesn't have bluetooth
    browser = webdriver.Chrome(options=options) # Need to use chromium webdriver since these websites load stock dynamically
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, "html.parser")

    price = soup.find('meta', property='og:price:amount')
    if (str(price) == 'None'): # Some are a bit different
        price = soup.find('meta', property='product:price:amount')
    price = price["content"]
    # These websites are all a bit different so will go through each. Although it is less efficient, it makes the code shorter
    stock = soup.find(attrs={'class':'stock_quantity'}) # New Realm Games
    if (str(stock) != 'None'): 
        stock = list(stock.stripped_strings)
        if (stock == []):
            stock = "Sold Out"
        else:
            stock = stock[0] + " in stock"
    else:
        stock = soup.find(attrs={'class':'form-field--stock'}) # Face to Face Games
        if (str(stock) != 'None'):
            stock = list(list(list(stock.children)[1])[1].stripped_strings)[0] + " in stock"
        else:
            stock = soup.find(attrs={'class':'product-vendor'}) # Cardboard Memories
            if (str(stock) != 'None'):
                stock = list(list(stock.children)[1].stripped_strings)[0]
            else:
                stock = "Not Found"
        
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)
    browser.close()


# Fox and Dragon Hobbies, Optimum Collection
urls = ['https://www.foxanddragonhobbies.ca/collections/pokemon-cards/products/presale-booster-box-chilling-reign-pokemon-cards',
'https://optimumcollection.ca/products/pokemon-chilling-reign-booster-box-pre-order'
]
for url in urls:
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Surpess bluetooth adapter error since my pc doesn't have bluetooth
    browser = webdriver.Chrome(options=options) # Need to use chromium webdriver since these websites load stock dynamically
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    price = soup.find('meta', property='og:price:amount')["content"]
    stock = list(soup.find(id='addToCart-product-template').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)
    browser.close()


# Infinity Cards & Collectibles, House of Cards, Miraj Trading, Duel Kingdom, K-OS Collectibles, Geekitude
urls = [#'https://www.infinitycards.ca/collections/booster-box/products/pre-order-swsh5-battle-styles-booster-box-releases-march-19-2021',
'https://houseofcards.ca/collections/pokemon-booster-boxes/products/sword-shield-chilling-reign-booster-box-preorder',
'https://www.mirajtrading.com/collections/pokemon/products/pokemonswordshieldchillingreignboosterbox',
'https://duelkingdom.ca/collections/pokemon-booster-boxes/products/pokemon-tcg-sword-shield-chilling-reign-booster-box',
'https://koscollectibles.ca/collections/pokemon/products/sword-and-shield-vivid-voltage-booster-box',
'https://geekittude.com/products/pokemon-sword-shield-chilling-reign-booster-box'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.find('meta', property='og:price:amount')
    if (str(price) == 'None'): # Miraj Trading and K-OS Collectibles are a bit different
        price = soup.find('meta', property='product:price:amount')
    price = price["content"]
    stock = soup.find(attrs={'class':'button--disabled'})
    if (str(stock) != 'None'): # Out of stock, add to cart button is disabled
        stock = "Sold Out"
    else:
        stock = list(soup.find(attrs={'data-action':'add-to-cart'}).stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# J&J and Prisma TCG
urls = [#'https://shop.jjcards.com/Pokemon-Sword-Shield-Battle-Styles-Booster-Box_p_20799.html',
'https://www.prismatcg.com/chilling-reign-pokemon-tcg-booster-box-w2'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = list(soup.find(id='price').stripped_strings)[0]
    stock = list(soup.find(id='availability').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# Jeux3Dragons, TopDeck Hero, Gods Arena, Dolly's, The Toy Trove, Dragon World, and Atlas Collectables
urls = ['https://www.jeux3dragons.com/catalog/pokemon_sealed_products/sword__shield_chilling_reign_booster_box/497704',
'https://www.topdeckhero.com/catalog/pokemon_sealed_products-pokemon_booster_box/chilling_reign_booster_box/477706',
'https://www.godsarena.com/catalog/pokemon_sealed_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/1706783',
'https://www.dollys.ca/catalog/pokemon_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/741283',
'https://www.thetoytrove.com/catalog/pokemon_sealed_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/2043790',
'https://dragontcg.crystalcommerce.com/catalog/pokemon_sealed_products__u-pokemon_booster_boxes/pokemon_swsh6_chilling_reign_booster_box/2052236',
#'https://www.atlascollectables.com/catalog/pokemon_sealed_products-pokemon_booster_boxes/sword__shield__battle_styles_booster_box/2043841'
]
for url in urls:
    header = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'
    }
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    stock = soup.select("span.price.no-stock") # select multiple classes
    price = ""
    if (stock != []): # out of stock
        price = list(stock[0].stripped_strings)[0]
        stock = "Sold Out"
    else: # in stock
        price = list(soup.find(attrs={'class':'regular price'}).stripped_strings)[0]
        stock = soup.find(attrs={'name':'qty'})["max"] + " in stock"
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# The Cards Vault and HappyTCG
urls = ['https://thecardsvault.com/product/pre-order-pokemon-chilling-reign-booster-box-available',
'https://happytcg.ca/shop/pokemon-tcg/latest-sets/chilling-reign/sword-shield-chilling-reign-booster-box-pre-order/'
]
for url in urls:
    header = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'
    }
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    price = list(soup.find('p', {'class':'price'}).descendants)
    length = len(price)
    price = price[length - 1] # Price is always last item in list
    stock = soup.find(attrs={'class':'in-stock'})
    if (str(stock) != 'None'):
        stock = list(stock.stripped_strings)[0]
    else:
        stock = "Sold Out"
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# KD Collectibles, Game Palace, Skyfox Games
urls = ['https://kdcollectibles.ca/collections/pokemon-booster-boxes/products/chilling-reign-booster-box-ships-immediately',
'https://gamepalace.ca/products/pre-order-pokemon-chilling-reign-booster-box?_pos=1&_sid=d0c3e4848&_ss=r&variant=39927348232388',
'https://skyfoxgames.com/collections/booster-box/products/pokemon-chilling-reign-booster-box-pre-order'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.find('meta', property='og:price:amount')["content"]
    stock = list(soup.find(id='AddToCartText').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# BreakawaySC and Zephr Epic
urls = ['https://breakawaysc.com/product/pokemon-sword-and-shield-chilling-reign-booster-box/',
'https://zephyrepic.com/product/pokemon-sword-and-shield-chilling-reign-booster-box-raffle-item/'
]
for url in urls:
    # Need to pretend to be a web browser and breakawaysc doesn't allow automated python requests
    header = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'
    }
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    price = list(soup.find('bdi').children)[1]
    stock = soup.find('div', {'class':'out-of-stock'})
    if (str(stock) != 'None'):
        stock = soup.find('input', {'name':'quantity'})["max"] + " in stock"
    else:
        stock = "Sold Out"
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# SP Shop and 401 Games
urls = ['https://www.spshop.ca/collections/booster-boxes/products/pokemon-chilling-reign-booster-box',
'https://store.401games.ca/collections/pokemon-sealed-product/products/pokemon-chillingreign-boosterbox'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = list(soup.find(id='ProductPrice-product-template').stripped_strings)[0]
    stock = list(soup.find(id='AddToCartText-product-template').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# result = (price, stock, title)
# Filter prices
index = 0
while index < len(results):
    results[index][0] = re.sub("[^0-9,.]", "", results[index][0])
    index += 1

# Sort by price
def get_price(result):
    return result[0]

results.sort(key=get_price)

# Align titles
longestStoreName = 0
longestPrice = 0
for result in results:
    # Find longest store name
    if (len(result[2]) > longestStoreName): 
        longestStoreName = len(result[2])
    # Find longest price
    if (len(result[0]) > longestPrice): 
        longestPrice = len(result[0])

        
# Write results
f = open("results.txt", "w")
f.truncate(0)
for result in results:
    f.write(result[2])
    spacesLineup = longestStoreName - len(result[2])
    for i in range(spacesLineup): # Pad everything to be equal to longest store name
        f.write(' ')
    f.write('\t\t\t')
    f.write(result[0])
    spacesLineup = longestPrice - len(result[0])
    for i in range(spacesLineup): # Pad everything to be equal to longest price
        f.write(' ')
    f.write('\t\t\t')
    f.write(result[1])
    f.write('\n')
f.close()
