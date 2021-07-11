import requests
from bs4 import BeautifulSoup

results = []
urls = ['https://store.401games.ca/collections/pokemon-sealed-product/products/pokemon-chillingreign-boosterbox',
'https://www.spshop.ca/collections/booster-boxes/products/pokemon-chilling-reign-booster-box']

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