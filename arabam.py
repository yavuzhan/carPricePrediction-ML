# -*- coding: utf-8 -*-
# yavuzhan arabam.com Ford Focus webscrap & append to csv
import re
import urllib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# if would like creating new csv
'''
filename1 = "arabam.csv"
f = open(filename1, "w") # for write
headers = "year,km,cc,fuel,price\n"
f.write(headers)
f.close()
'''
# if would like appending the data to the created csv
filename1 = "S_sahibinden.csv"

''' URL Part '''
my_url = "https://www.arabam.com/ikinci-el/otomobil/ford-focus?sort=priceTl.asc&page=1"
proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
#opening up connection, grabbing the page.
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
souped_page = soup(page_html, "html.parser") #html parsing

#grabs each product (find sth)
#findAll("TAG NAME", {"LOOK FOR ALL ...(EX: class)ES":"GO THEM START WITH ....(EX:ITEM TITLE)"})
containers = souped_page.findAll("li", {"class" :"hide-on-parent-collapse"}) #The box includes ford focus sub models

#Lists for saving the models and their car size
category_list = list ()
category_have_list = list()
rounded_category_have_list = list() # page number

# This part includes parsing methods for cathing model names text and car range that having the models
for i in range(len(containers)):
    parsed_containers = re.split("                                    ",containers[i].text)
    second_parsed_containers = re.split("\r",parsed_containers[1]) # for which ford focus model
    second_parsed_containers_2 = re.split("\r",second_parsed_containers[0])
    category = second_parsed_containers_2[0].replace(".", "-",1)
    category = category.replace(" ", "-",1)
    category_list.append(category) # category names adding category_list

    third_parsed_containers = re.split("\"r",parsed_containers[2]) # for how many car having by the ford focus model
    third_parsed_containers_2 = re.split("\(",third_parsed_containers[0])
    category_have = third_parsed_containers_2[1].replace(")", "",1)  #.format(term=keyword.strip().replace(" ", "+"),
    category_have =  category_have.replace(".", "",1)
    category_have_list.append(float(category_have))

# Modifying category's ranges for using in url
for i in range(len(category_have_list)):
    divided_category = int(category_have_list[i]/20)
    rounded_category_have_list.append(divided_category+1) # arabam.com's each page has 20 car.


for i in range(len(rounded_category_have_list)):
#for i in range(0,1):
    print("i = ",i)
    tam = str(category_list[i])
    for j in range(0,int(rounded_category_have_list[i])):
        print("i = ",i)
        print(tam+":")
        print("The page is:", j+1)
        my_url = "https://www.arabam.com/ikinci-el/otomobil/ford-focus-"+tam+"?sort=priceTl.asc&page="+str(j+1)
        # print(my_url)
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        #opening up connection, grabbing the page.
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        #html parsing
        souped_page = soup(page_html, "html.parser")

        #grabs each product (find sth)
        #finAll("TAG NAME", {"LOOK FOR ALL ...(EX: class)ES":"GO THEM START WITH ....(EX:ITEM TITLE)"})
        #the class(box) includes each car's informations
        containers = souped_page.findAll("a", {"class" :"w100 smaller-text-slim bold"})

        #the class(box) includes each car's title
        car_model = (containers[0].text)

        #the class(box) includes each car's price
        price_containers = souped_page.findAll("td", {"class" :"tac p4 no-wrap semi-bold color-red4"})

        #the page has 20 car the containers contains 60 item. For each car -> 0: km , 1: color , 2:date
        km_containers = souped_page.findAll("td", {"class" :"tac p4 word-break"})

        #the class(box) includes each car's year and location , if even : year, odd : location
        year_containers = souped_page.findAll("td", {"class" :"tac p4"})

        # creation lists for each car data
        # li[3] : yil, li[4] : km , li[6] : yakit , li[7] : vites ,li[8] : motor , li[9] : hp
        title_list = list()
        price_list = list()
        year_list = list()
        km_list = list()
        fuel_list = list()
        #shift_list = list()
        cc_list = list()
        #hp_list = list()

        for i in range(len(containers)):
            title = containers[i].text
            title_parse = re.split(" ", title)
            cc = title_parse[2]

            # append title on title_list
            title_list.append(title)

            # append fuel on fuel_list
            if (title_parse[3] == "TDCi"):
                fuel_list.append("-1")  # if disel  -1
            else:
                fuel_list.append("1")   # else gasoil 1
            #print(str(i) + " " + fuel_list[i] + "-"+ title_list[i])

            # append cc on cc_list
            cc_list.append(cc)


        # append price on price_list
        for i in range(len(price_containers)):

            price_parse = re.split("\n", price_containers[i].text)
            price_parsed = re.split(" ", price_parse[1])
            price = price_parsed[0]
            price_list.append(price)


        # append year on year_list
        for i in range(len(year_containers)):
            year_parse = re.split("\n", year_containers[i].text)
            year_parsed = re.split(" ", year_parse[0])
            if (i%3==0):
                year = year_parsed[0]
                year_list.append(year)

        # append km on km_list
        for i in range(len(km_containers)):
            km_parse = re.split("\n", km_containers[i].text)
            km_parsed = re.split(" ", km_parse[0])
            km_parsed =  km_parsed[0].replace(".", "",1)  # remove . (Ex: 85.000 -> 85000)
            if (i%2==0):
                km = km_parsed
                km_list.append(km)

        # append each page to file
        for i in range(len(title_list)):
            f = open(filename1, "a")
            #f.write(title_list[i] + "," + price_list[i] + "," + year_list[i] + "," + km_list[i] + "," + fuel_list[i] +  "," + cc_list[i] +  "\n")
            f.write(year_list[i] + "," + km_list[i] + "," + cc_list[i]+ "," + fuel_list[i] + "," + price_list[i] + "\n" )
            f.close()

        #print(len(title_list),len(price_list), len(year_list),len(km_list),len(fuel_list),len(cc_list))
        #print(price_list,year_list,km_list,cc_list,fuel_list)
        #print("\n")
