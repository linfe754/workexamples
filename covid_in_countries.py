# This script can get covid stats overviews in countries of selection.

import pandas as pd
import numpy as np
from datetime import date

def covid_in_country(country):

    if " " in country:
        country_in_url = country.replace(" ","%20")
    else:
        country_in_url = country
    
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/'+country_in_url+'.csv'
    vax = pd.read_csv(url)

    vax_people_num = vax['people_vaccinated'].tolist()
    vaxed_population = np.nanmax(vax_people_num)
    vax_date_list = vax['date'].tolist()
    vax_date = vax['date'].values[vax[vax['people_vaccinated']==vaxed_population].index.values[0]]

    covid_data = pd.read_csv("https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv")
    covid_country = covid_data[covid_data['location']==country]
    population = np.mean(covid_country['population'])

    vax_rate = round(vaxed_population/population*100,2)

    vax_people_7 = vax_people_num[-7]
    vax_people_30 = vax_people_num[-30]

    new_cases = covid_country['new_cases'].tolist()
    avg_30 = np.mean(new_cases[-30:])
    avg_7 = np.mean(new_cases[-7:]) 

    print("-"*50)
    print("Date: ", date.today())
    print("Country: "  + country)
    print("Cases 7-day average: ", round(avg_7,2))
    print("Cases 30-day average: ", round(avg_30,2))    
    print("Lastest reported vaccinated rate: "+ str(vax_rate)+ "% on "+ vax_date)

    if np.isnan(vax_people_7):
        print("Vaccinated rate on "+vax_date_list[-7]+": ","Not Reported")
    else:
        print("Vaccinated rate on "+vax_date_list[-7]+": ",round(vax_people_7/population*100,2))

    if np.isnan(vax_people_30):
        print("Vaccinated rate on "+vax_date_list[-30]+": ","Not Reported")
    else:
        print("Vaccinated rate on "+vax_date_list[-30]+": ",round(vax_people_30/population*100,2))
    print('')
    
    
# countries of interest    
countries = ['China', 'Australia', 'United States', 'United Kingdom',  'New Zealand', 'Japan', 'Germany', 'France', 'Singapore']

for x in countries:
    covid_in_country(x)  

    
    
    
