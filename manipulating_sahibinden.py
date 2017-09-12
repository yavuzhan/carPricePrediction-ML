# -*- coding: utf-8 -*-
# manipulating the data for features are on a similar scale
import pandas as pd

data = pd.read_csv('C:\\Users\\Yavuzhan\\Desktop\\DataMining_codes\\sahibinden\\S_sahibinden.csv', index_col = False) # , index_col = False
df = pd.DataFrame(data)

#manipulating price
price_max = df.price.max()
price_min = df.price.min()
price_mean= df.price.mean()
#df.price = ((df.price - price_mean) / (price_max - price_min)).round(3) # with mean normalization
df.price = (df.price / (price_max - price_min)).round(3) #without mean normalization


#manipulating km
km_max = df.km.max()
km_min = df.km.min()
km_mean = df.km.mean()
df.km = ((df.km - km_mean) / (km_max - km_min)).round(3) #with mean normalization


#manipulating year
year_max = df.year.max()
year_min = df.year.min()
year_mean = df.year.mean()
df.year = ((df.year - year_mean) / (year_max - year_min)).round(3) #with mean normalization


#manipulating cc
cc_max = df.cc.max()
cc_min = df.cc.min()
cc_mean = df.cc.mean()
df.cc = ((df.cc ) / (cc_max - cc_min)).round(3)  #without mean normalization


#manipulating fuel
fuel_max = df.fuel.max()
fuel_min = df.fuel.min()
df.fuel = ((df.fuel) / ( fuel_max - fuel_min))  #without mean normalization

#writing to new csv
df.to_csv('manipulated_sahibinden.csv')
