import requests
from bs4 import BeautifulSoup

results = []

urls = ['https://breakawaysc.com/product/pokemon-sword-and-shield-evolving-skies-booster-box/',
#'https://zephyrepic.com/product/pokemon-sword-and-shield-chilling-reign-booster-box-raffle-item/'
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
        stock = "Out of stock"
    title = soup.find('meta', property='og:site_name')["content"]
    data = (price, stock, title)
    results.append(data)


urls = [#'https://www.spshop.ca/collections/booster-boxes/products/pokemon-chilling-reign-booster-box',
'https://store.401games.ca/collections/pokemon-sealed-product/products/pokemon-evolving-skies-booster-box-pre-order'
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
