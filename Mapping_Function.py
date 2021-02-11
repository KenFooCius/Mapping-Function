#This is the Near Me Function for Health AI, which can ID 5 mile clusters for number of people using the app and the percent who has COVID
#This is written by Ken Foo and used for Christopher H to integrate to Google Maps

#import computational and mapping libraries
import math
import numpy as np
import pandas as pd
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for geospatial
import folium
import geopy
## for machine learning
from sklearn import preprocessing, cluster
import scipy
## for deep learning
import minisom
from flask import Flask
from flask import request

#Read the csv file of the coffee stores (this is a placeholder fake data for people with COVID)
#dtf = pd.read_csv('stores_10_8_2020.csv')

test= Flask(__name__)

@test.route('/5mileMapping', methods=['POST'])
def makecalc():
    input = request.get_json(force=True)  #this takes the POST request from the body

    #pull in inputs needed to run the 5 mile cluster algorithm
    latitude= input['latitude']
    longitude= input['longitude']

    #Read the dataframe
    dtf = pd.read_csv('data_stores.csv')
    #dtf = dtf[dtf["City"]==filter][["City","Street Address","Longitude","Latitude"]].reset_index(drop=True)
    #dtf = dtf.reset_index().rename(columns={"index":"id"})




    # Locations_less_than_5_miles = []
    # for i in dtf['Longitude'][1:5]:
    #     for x in dtf['Latitude'][1:5]:
    #         Locations_less_than_5_miles.append(i)
    # return str(Locations_less_than_5_miles)


    #Tells you the data above is within 5 miles or not by outputting: True or False
    Locations_less_than_5_miles = []
    for i in dtf['Longitude'][1:5]:
        for x in dtf['Latitude'][1:5]:
            radiusEarth = 3961  # miles. If you want km, put in 6373 km in instead
            lat1 = math.radians(36.14)
            lon1 = math.radians(-115.19)
            lat2 = math.radians(x)  # plug and chug
            lon2 = math.radians(i)  # plug and chug
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = [round(radiusEarth * c, 2)]  # in miles
            Locations_less_than_5_miles.append(distance)
            # if distance < 5:  # 5 mile threshold
            #     Locations_less_than_5_miles.append(["True"])
            # else:
            #     Locations_less_than_5_miles.append(["False"])
    return str(Locations_less_than_5_miles)



    #Combine the data and the corresponding

    ID_Locations_less_than_5_miles = pd.Series(Locations_less_than_5_miles)
    dtf["Within_5_miles"] = ID_Locations_less_than_5_miles[:]  # Index the true and false for within 5 miles
    
    # This is a random string generator for the # of evaluations
    dtf["% of People Infected"] = np.random.choice(
        ["%80 > Infected", "%60 > Infected", "%40 > Infected", "%20 > Infected", "%20 < Infected"], size=len(dtf),
        p=[0.2, 0.2, 0.05, 0.40, 0.15])
    
    # dtf["# of People Processed"] = np.random.choice(["People using app:Greater than 66","People using app:Between 33-66","People using app:Lower than 33"], size=len(dtf), p=[0.4,0.45,0.15])
    
    # The fraction of people infected from the # of evaluations
    dtf["# of People Processed"] = np.random.randint(low=0, high=100, size=len(dtf))
    # Display only data points within 5 miles only!
    dtf[dtf.Within_5_miles == True]

test.run(debug=True, port=5013)