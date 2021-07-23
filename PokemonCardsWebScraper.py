import requests
import json
import re
from Url import *
from bs4 import BeautifulSoup
from selenium import webdriver

results = []

# Red Nails 2
urls = [RedNails2
]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [KanzenGames, SkafExpress]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [WizardsTower]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [GameShack]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find(attrs={'class':'add-to-cart-wrapper'}) # Only way to find the right price since website is weird with prices
    price = list(data.find(attrs={'class':'price'}).stripped_strings)[0]
    stock = list(list(data.find(attrs={'class':'availability'}).children)[1].stripped_strings)[0]
    title = list(list(soup.find(attrs={'class':'logo'}).children)[0].stripped_strings)[0]
    data = [price, stock, title]
    results.append(data)


# The League's Den
urls = [TheLeaguesDen]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [NewRealmGames,CardboardMemories,FaceToFaceGames]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [FoxAndDragonHobbies,OptimumCollection]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [InfinityCardsAndCollectibles,HouseOfCards,MirajTrading,DuelKingdom,KOSCollectibles,Geekitude]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [JandJCollectibles, PrismaTCG]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = list(soup.find(id='price').stripped_strings)[0]
    stock = list(soup.find(id='availability').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# Jeux3Dragons, TopDeck Hero, Gods Arena, Dolly's, The Toy Trove, Dragon World, and Atlas Collectables
urls = [Jeux3Dragons,TopDeckHero,GodsArena,Dollys,TheToyTrove,DragonWorld,AtlasCollectibles]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [TheCardsVault,HappyTCG]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [KDCollectibles,GamePalace,SkyFoxGames]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = soup.find('meta', property='og:price:amount')["content"]
    stock = list(soup.find(id='AddToCartText').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# BreakawaySC and Zephr Epic
urls = [BreakawaySC, ZephyrEpic]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
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
urls = [SPShop, The401Games]
for url in urls:
    if (url == ''): # Skip website if blank
        continue
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price = list(soup.find(id='ProductPrice-product-template').stripped_strings)[0]
    stock = list(soup.find(id='AddToCartText-product-template').stripped_strings)[0]
    title = soup.find('meta', property='og:site_name')["content"]
    data = [price, stock, title]
    results.append(data)


# data = (price, stock, title)
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
