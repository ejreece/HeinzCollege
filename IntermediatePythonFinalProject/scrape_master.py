### Web Scraping
## Last updated 2/26/2020

#--------------------------------------------------------------
# import necessary packages
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
#--------------------------------------------------------------

## Pittsburgh Magazine 2019 Best Restaurants
# use requests to download the webpage
page19 = requests.get("https://www.pittsburghmagazine.com/best-restaurants-in-pittsburgh-in-2019/")

# use BeautifulSoup to parse the page
soup19 = BeautifulSoup(page19.content, 'html.parser')
article19 = soup19.find(id="post-10065")

# pull and clean restaurant names
h3s19 = article19.find_all('h3')
h3s19 = h3s19[2:]
restNames19 = []
for i in range(len(h3s19)):
    name19 = h3s19[i].get_text()
    if re.search('\\xa0', name19) != None:
        name19 = name19.replace('\xa0', ' ')
    restNames19.append(name19)
restNames19[7] = 'DIANOIAS EATERY'
restNames19[13] = 'FL. 2'
restNames19[16] = 'LEGUME'
restNames19[18] = 'POULET BLEU'
restNames19[19] = 'SALEMS MARKET & GRILL'

# convert article to string
articleStr19 = soup19.find(id="post-10065").get_text()      

# pull and clean restaurant phone numbers
phoneNums = re.findall('\d{3}/\d{3}-\d{4}', articleStr19)
phoneNums19 = []
for n in phoneNums:
    phoneNum = n[0:3] + n[4:7] + n[8:]
    phoneNums19.append(phoneNum)
phoneNums19.insert(restNames19.index('APTEKA'), 'No Phone')
phoneNums19.insert(restNames19.index('BITTER ENDS LUNCHEONETTE'), 'No Phone')

# pull and clean restaurant cuisines
cuisines19 = re.findall('Cuisine.*\n', articleStr19)
cuisineNames19 = []
for c in cuisines19:
    cuisine19 = c.lstrip('Cuisine:').strip(' ').lstrip('\xa0').rstrip('\n').lstrip(' ')
    cuisineNames19.append(cuisine19.upper())
cuisineNames19[-6] = 'NEW AMERICAN'

# pull and clean restaurant descriptions
articleStr19_2 = str(soup19.find(id="post-10065"))
descrips19 = re.findall(r'.\xa0 </strong></p>\n<p>(.+?)</p>|.\xa0</strong></p>\n<p>(.+?)</p>|.</strong></p>\n<p>(.+?)</p>', articleStr19_2)
restDescrips19 = []
for tup in descrips19:
    for item in tup:
        if len(item) > 1:
            restDescrips19.append(item)
for item in restDescrips19:
    if item[0] == '<':
        restDescrips19.remove(item)
restDescrips19[12] = re.sub(', <strong>.*</strong>,','',restDescrips19[12])

#--------------------------------------------------------------
## Pittsburgh Magazine 2018 Best Restaurants
# Create the http request and request the page
httpString18 ='https://www.pittsburghmagazine.com/best-restaurants-2018/'
page18 = requests.get(httpString18)
soup18 = BeautifulSoup(page18.content, 'html.parser')
article18 = soup18.find(id="post-8871")

# Scrape Restaurant Names
restMessy = article18.find_all("h3")
restClean1 = list()
for i in restMessy:
    restClean1.append(i)
restClean2 = list()
for i in restClean1:
    a = str(i)
    b = a[4:]
    c = b[:-5]
    restClean2.append(c)

# Clean Restaurant Names
Casbah = restClean2[4]
restClean2[4] = Casbah[0:6]
restClean2[27] = 'Bitter Ends Garden & Luncheonette'
restClean2[32] = 'Salems Market & Grill'
restClean2[33] = 'Tessaros American Bar & Hardwood Grill'
# Insert Stagioni to the list
restClean2a = restClean2[0:10]
restClean2b = restClean2[10:]
restClean2a.append('Stagioni')
restClean3 = restClean2a + restClean2b
restClean3[20] = 'Cocothe'
restClean3[14] = 'Dianoias Eatery'
restClean18 = list()
for rest in restClean3:
    if re.search('\'', rest) != None:
        name19 = name19.replace('\'', '')
    restClean18.append(rest.upper())
    
# Use regex to find restaurant phone numbers
articleString18 = str(article18)
phoneNums0 = re.findall('\d{3}/\d{3}-\d{4}',articleString18)
phoneNums18 = list()
for num in phoneNums0:
    numNew = num[0:3] + num[4:7] + num[8:]
    phoneNums18.append(numNew)
# Insert 'No Phone' for Apteka & Noodlehead
Apteka = restClean18.index('APTEKA')
Noodlehead = restClean18.index('NOODLEHEAD')
phoneNums1 = phoneNums18[0:Apteka]
phoneNums1.append('No Phone')
phoneNums2 = phoneNums18[Apteka:Noodlehead]
phoneNums2.append('No Phone')
phoneNums3 = phoneNums18[Noodlehead:]
phoneNumsClean18 = phoneNums1 + phoneNums2 + phoneNums3

# Use regex to find restaurant cuisine types
cuisines = re.findall('\[[a-zA-Z]+[/]*[a-zA-Z]+[^\S]*[a-zA-Z]+\]',articleString18)
# Remove brackets from each cuisine
cuisinesClean18 = list()
for i in cuisines:
    newi = i[1:-1]
    cuisinesClean18.append(newi.upper())

# Use regex to find restaurant descriptions
descrips18 = re.findall(r'</strong>(.+?)</p>', articleString18)
# Remove indent (whitespace) from description paragraphs
descripsClean18 = list()
for i in descrips18:
    newi = i.lstrip()
    descripsClean18.append(newi)
# Clean up Superior Motors & fl. 2 descriptions (contained hyperlinks)
supMotors = restClean18.index('SUPERIOR MOTORS')
fl2 = restClean18.index('FL. 2')
descripsClean18[supMotors] = 'Executive Chef/Co-Owner Kevin Sousa serves New American cuisine influenced by modernist technique at his Braddock establishment, which the independent Restaurant Review Panel selected as this year’s Best New Restaurant. Sousa’s artfully composed dishes such as carrot or tuna tartare with nori, kimchi, miso and katsuobushi and sturgeon with spaetzle, cauliflower, cabbage and mustard are a draw to the restaurant, as is Superior Motors’ forward-thinking cocktail program.'
descripsClean18[fl2] = 'Architect Lázaro Rosa-Violán’s stunning redesign transformed the restaurant space at the Fairmont Pittsburgh into Pittsburgh Magazine’s 2018 Delicious Design winner. Executive Chef Julio Peraza’s dinner menu includes shareable main courses such as a whole rotisserie chicken served with an herb salad and braised lamb shank with white-bean stew and double-smoked bacon, as well as delicate dishes such as scallop crudo and cured kampachi. We also love fl.2 for an elegant yet casual lunch or brunch; it’s a perfect spot for a business meeting or quick catch up with a friend.'
#--------------------------------------------------------------
    
## Master Restaurants List
# create dataframes
rests2019 = pd.DataFrame({'Name': restNames19, 'Cuisine': cuisineNames19, 'Phone Number': phoneNums19, 'Description': restDescrips19})
rests2018 = pd.DataFrame({'Name': restClean18, 'Cuisine': cuisinesClean18, 'Phone Number': phoneNumsClean18, 'Description': descripsClean18})

# merge dataframes (THIS WORKS)
restData = pd.concat([rests2019, rests2018], ignore_index=True)
restData.sort_values(by=['Name'], inplace=True)
restData.reset_index(drop=True, inplace=True)

# create twice rated column (THIS ALSO WORKS)
unique = restData['Name'].duplicated(keep=False).copy()
restData['Twice Rated'] = unique

# drop restaurants without phone numbers (SAME HERE)
missing = restData[restData['Phone Number']=='No Phone'].index
restData.drop(missing, inplace=True)

# reset the index (YUP)
restData.reset_index(drop=True, inplace=True)

# drop duplicates (THIS IS WHERE IT ALL GOES WRONG)
restData.drop_duplicates(['Name'], inplace=True)

# export dataframe into CSV called restaurantDF
restData.to_csv('restData.csv', index=False)