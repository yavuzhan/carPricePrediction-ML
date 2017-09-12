# yavuzhan sahibinden.com Ford Focus webscrap & write to csv
import urllib.parse
import urllib.request
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

filename1 = "S_sahibinden.csv"
f = open(filename1, "w") # for write
headers = "year,km,cc,fuel,price\n" # creating header
f.write(headers)
f.close()
''' URL Part '''
url = "https://www.sahibinden.com/ford-focus?sorting=price_asc"
print(url + "\n")
user_agent = 'Chrome/5.0 (Windows NT 6.3; Win64; x64)'
values = {'name' : 'Michael Foord',
           'location' : 'Northampton',
           'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = urllib.request.Request(url, data, headers)
uClient = uReq(req)
page_html = uClient.read()
uClient.close()

'''
with urllib.request.urlopen(req) as response:
   the_page = response.read()
#print(the_page)
'''
souped_page = soup(page_html, "html.parser") #html parsing

#grabs each product (find sth)
#finAll("TAG NAME", {"LOOK FOR ALL ...(EX: class)ES":"GO THEM START WITH ....(EX:ITEM TITLE)"})
containers = souped_page.findAll("li", {"class" :"cl4"}) #The box includes ford focus sub models

#Lists for saving models and their car size
category_list = list () # which sub model
category_have_list = list() # car size
rounded_category_have_list = list() # page number

# This part includes parsing methods for cathing model names text and car range that having the models
for i in range(int(len(containers)/2)):
    parsed_containers = re.split("                                                ",containers[i].text)
    second_parsed_containers = re.split("\(",parsed_containers[1])
    third_parsed_containers = re.split("\n",second_parsed_containers[0]) # for which ford docus model
    third_parsed_containers_2 = re.split("\)",second_parsed_containers[1]) # for how many car having by the ford focus model
    category = third_parsed_containers[0]   # ['1.0 GTDi', '1.4', '1.5 TDCi', '1.6', '1.6 SCTi', '1.6 TDCi', '1.6 Ti-VCT', '1.8 TDCi', '2.0', '2.3', '2.5']
    category = category.replace(" ", "-",1) # for changing the blanks wtih "-" using in url links
    category_list.append(category) # category names adding category_list
    category_have = third_parsed_containers_2[0]
    category_have = category_have.replace(".", "",1)
    category_have_list.append(float(category_have))

# Modifying category's ranges for using in url
for i in range(len(category_have_list)):
    divided_category = int(category_have_list[i]/20)
    rounded_category_have_list.append(divided_category+1) # sahibinden.com's each page has 20 car.
    '''
    if divided_category == 0 :
        divided_category = divided_category +1 # if rounded page is 0 , this page' s car couldnt catch, so added +1
    rounded_category_have_list.append(divided_category) # sahibinden.com's each page has 20 car.
    '''

for i in range(len(rounded_category_have_list)):
    print("i = ",i)
    tam = str(category_list[i]) # car model 1.0 gtdi , 1.5 tdci etc..
    for j in range(0,int(rounded_category_have_list[i])):
        if j<50: # sahibinden.com shows max 50 page.
            print(tam+":" )
            print("The page is:", j)
            car_url = "https://www.sahibinden.com/ford-focus-"+tam+"?pagingOffset="+str(j*2)+"0&sorting=price_asc"
            print(car_url + "\n")

            ''' URL Part '''
            user_agent = 'Chrome/5.0 (Windows NT 6.3; Win64; x64)'
            values = {'name' : 'Michael Foord',
                      'location' : 'Northampton',
                      'language' : 'Python' }
            headers = { 'User-Agent' : user_agent }
            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')
            req = urllib.request.Request(car_url, data, headers)
            uClient = uReq(req)
            page_html = uClient.read()
            uClient.close()

            #html parsing
            souped_page = soup(page_html, "html.parser")
            #grabs each product (find sth)
            #finAll("TAG NAME", {"LOOK FOR ALL ...(EX: class)ES":"GO THEM START WITH ....(EX:ITEM TITLE)"})

            #the class(box) includes each car's informations
            containers = souped_page.findAll("tr", {"class" :"searchResultsItem "})

            #the class(box) includes each car's title
            # title containerstaki 0,2,4.. Taunus vb ; 1,3,5  2.0 tdi etc
            title_containers = souped_page.findAll("td", {"class" :"searchResultsTagAttributeValue"})

            #the class(box) includes each car's km, year etc..
            # km, year vs cekilecek container s
            # when the page has 20 car the containers contains 60 item. For each car -> 0: year , 1: km , 2:color
            datas_containers = souped_page.findAll("td", {"class" :"searchResultsAttributeValue"})


            #the class(box) includes each car's price
            price_containers = souped_page.findAll("td", {"class" :"searchResultsPriceValue"})
            price_parsed = re.split(" ",price_containers[0].text)


            # creation lists for each car data
            title_list = list()
            price_list = list()
            year_list = list()
            km_list = list()
            fuel_list = list()
            #shift_list = list()
            cc_list = list()
            #hp_list = list()

            # Each page has 20 car
            for i in range(len(title_containers)):
                # parsing
                title_parsed = re.split("                        ",title_containers[i].text)
                title_parsed_1 = title_parsed[1]
                title_split = re.split(" ", title_parsed_1)
                title_0 = title_split[0]
                # each car's title is appended to title_list
                title_1 = title_split[1]
                mystring = str(title_parsed_1)
                myremove = str(title_split[0])
                removed = mystring.replace(myremove,"",1)
                title = removed.replace(" ", "",1)
                title_list.append(title)

                # each car's cc is appended to cc_list
                cc = title_0
                cc_list.append(cc)

                # each car's fuel is appended to fuel_list
                fuel_parsed = re.split(" ", title)
                if (fuel_parsed[0] == "TDCi"):
                    fuel_list.append("-1") # if disel  -1
                else:
                    fuel_list.append("1") # else gasoil 1



            # when the page has 20 car the containers contains 60 item. For each car -> 0: year , 1: km , 2:color
            # each car year is appended to year_list , each car km is appended to km_list
            for i in range(len(datas_containers)):
            # each car year is appended to year_list
                if (i%3 == 0):
                    year_parsed = re.split("                    ",datas_containers[i].text)
                    year = year_parsed[1]
                    year_list.append(year)

                # each car km is appended to km_list
                elif (i%3==1):
                    km_parsed = re.split("                    ",datas_containers[i].text)
                    km = km_parsed[1]
                    km_list.append(km)


            # each car's price is appended to price_list
            for i in range(len(price_containers)):
                price_parsed = re.split(" ",price_containers[i].text)
                price = price_parsed[1]
                price_list.append(price)

            # append each page to file
            for i in range(len(containers)):
                f = open(filename1, "a")
                f.write(year_list[i] + "," + km_list[i] + "," + cc_list[i]+ "," + fuel_list[i] + "," + price_list[i] + "\n" )
                f.close()
            #print(price_list,year_list,km_list,cc_list,fuel_list)
            #print("\n")
