import requests
from bs4 import BeautifulSoup

results = []


# Jeux3Dragons, TopDeck Hero, Gods Arena, Dolly's, The Toy Trove, and Dragon World
urls = ['https://www.jeux3dragons.com/catalog/pokemon_sealed_products/sword__shield_chilling_reign_booster_box/497704',
'https://www.topdeckhero.com/catalog/pokemon_sealed_products-pokemon_booster_box/chilling_reign_booster_box/477706',
'https://www.godsarena.com/catalog/pokemon_sealed_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/1706783',
'https://www.dollys.ca/catalog/pokemon_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/741283',
'https://www.thetoytrove.com/catalog/pokemon_sealed_products-pokemon_booster_boxes/sword__shield_chilling_reign_booster_box/2043790',
'https://dragontcg.crystalcommerce.com/catalog/pokemon_sealed_products__u-pokemon_booster_boxes/pokemon_swsh6_chilling_reign_booster_box/2052236',
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
    data = (price, stock, title)
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
    price = list(soup.find('p', {'class':'price'}).descendants)[4]
    stock = soup.find(attrs={'class':'in-stock'})
    if (str(stock) != 'None'):
        stock = list(stock.stripped_strings)[0]
    else:
        stock = "Sold Out"
    title = soup.find('meta', property='og:site_name')["content"]
    data = (price, stock, title)
    results.append(data)


# KD Collectibles and Game Palace
urls = ['https://kdcollectibles.ca/collections/pokemon-booster-boxes/products/chilling-reign-booster-box-ships-immediately',
'https://gamepalace.ca/products/pre-order-pokemon-chilling-reign-booster-box?_pos=1&_sid=d0c3e4848&_ss=r&variant=39927348232388'
]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = list(soup.find(id='ProductPrice').stripped_strings)[0]
    stock = list(soup.find(id='AddToCartText').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = (price, stock, title)
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
    if (stock != 'None'):
        stock = soup.find('input', {'name':'quantity'})["max"] + " in stock"
    else:
        stock = "Sold Out"
    title = soup.find('meta', property='og:site_name')["content"]
    data = (price, stock, title)
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
    data = (price, stock, title)
    results.append(data)


# Align titles
longest = 0
for result in results:
    if (len(result[2]) > longest):
        longest = len(result[2])
        
# Write results
f = open("results.txt", "w")
f.truncate(0)
for result in results:
    f.write(result[2])
    spacesLineup = longest - len(result[2])
    for i in range(spacesLineup):
        f.write(' ')
    f.write('\t\t\t')
    f.write(result[0])
    f.write('\t\t\t')
    f.write(result[1])
    f.write('\n')
f.close()
