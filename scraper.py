import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import model
import reactors as rea
import countries as c
import re

# webscarping class to grab data from website and insert into database

class Scraper:
    def country_data(self):
        url = 'https://en.wikipedia.org/wiki/Nuclear_power_by_country'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        table = soup.find_all('table')
        df = pd.read_html(str(table), header=0)
        jsondata = json.loads(df[1].to_json(orient='records'))
        code_url = 'https://countrycode.org/'
        code_r = requests.get(code_url)
        code_soup = BeautifulSoup(code_r.content, 'lxml')
        code_table = code_soup.find_all('table')
        code_df = pd.read_html(str(code_table), header=0)
        code_data = json.loads(code_df[1].to_json(orient='records'))
        coorurl = 'https://en.wikipedia.org/wiki/List_of_nuclear_power_stations'
        coorr = requests.get(coorurl)
        coorsoup = BeautifulSoup(coorr.content, 'lxml')
        coortable = coorsoup.find_all('table')
        coordf = pd.read_html(str(coortable), header=0)
        coorjsondata = json.loads(coordf[1].to_json(orient='records'))

        for i in jsondata:
            for j in code_data:
                if i['Country'] == j['COUNTRY']:
                    i['country_code'] = j['ISO CODES']



        countries = []
        print(jsondata)
        for i in range(1, len(jsondata)):
            country = jsondata[i]['Country']
            reactors = int(jsondata[i]['Reactors'] + jsondata[i]['Reactors.1'])
            capacity_total = jsondata[i]['CapacityNet-total (MWe)']  # strip and make only numbers
            generated_electricity = jsondata[i]['Generatedelectricity (GWh)']
            percent_use = jsondata[i]['Share of total electricity use']
            if 'country_code' in jsondata[i].keys():
                country_code = jsondata[i]['country_code'].split("/")[0].replace(" ","")
            else:
                country_code = None
            countries.append(c.Country(country, reactors, capacity_total, generated_electricity, percent_use, country_code))

        return countries

    def get_reactors(self):
        db = model.Database()
        con = db.get_country_codes()
        dict = {}
        reactors = []
        coorurl = 'https://en.wikipedia.org/wiki/List_of_nuclear_power_stations'
        coorr = requests.get(coorurl)
        coorsoup = BeautifulSoup(coorr.content, 'lxml')
        coortable = coorsoup.find_all('table')
        coordf = pd.read_html(str(coortable), header=0)
        coorjsondata = json.loads(coordf[1].to_json(orient='records'))


        for i in range(0, len(con)):
            if con[i][0] is not None:
                url = 'https://pris.iaea.org/PRIS/CountryStatistics/CountryDetails.aspx?current=' + con[i][0].replace(" ",
                                                                                                                    "")
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'lxml')
                table = soup.find_all('table')
                df = pd.read_html(str(table), header=0)
                jsondata = json.loads(df[3].to_json(orient='index'))
                dict[con[i][0].replace(" ", "")] = jsondata

        # manipulate json data and add country id to the reactors from the countries table
        print(coorjsondata)
        # for j in range(0, len(coorjsondata)):
        #     for i in con[0]:
        #         print(coorjsondata[j])
        #         print(dict[i]['0'])
        #         if coorjsondata[j]['Power station'].upper() in i[1].upper():
        #             lat = j['Location'].upper().split("/")[1].split(" ")[1]
        #             long = j['Location'].upper().split("/")[1].split(" ")[2]
        #             i['lat'] = long
        #             i['long'] = lat
        #             print(i)

        for i in range(0, len(con)):
            if con[i][0] is not None:
                for j in range(0, len(dict[con[i][0].replace(" ", "")])):
                    dict[con[i][0].replace(" ", "")][str(j)]['ID'] = con[i][1]
                    name = dict[con[i][0].replace(" ", "")][str(j)]['Name']
                    reactorType = dict[con[i][0].replace(" ", "")][str(j)]['Type']
                    status = dict[con[i][0].replace(" ", "")][str(j)]['Status']
                    location = dict[con[i][0].replace(" ", "")][str(j)]['Location']
                    rup = dict[con[i][0].replace(" ", "")][str(j)]['Reference Unit Power  [MW]']
                    gec = dict[con[i][0].replace(" ", "")][str(j)]['Gross Electrical Capacity [MW]']
                    fgc = dict[con[i][0].replace(" ", "")][str(j)]['First Grid Connection']
                    id = dict[con[i][0].replace(" ", "")][str(j)]['ID']
                    for z in coorjsondata:
                        # print(name.upper(), z['Power station'].upper())
                        if z['Power station'].upper() in name.upper():
                            # print(name.upper(), z['Power station'].upper())
                            lat = z['Location'].split("/")[1].split(" ")[1]
                            long = z['Location'].split("/")[1].split(" ")[2]
                            if "S" in lat:
                                lat = float(re.findall("[0-9]*\.[0-9]*",lat)[0]) * -1
                            else:
                                lat = float(re.findall("[0-9]*\.[0-9]*",lat)[0])
                            if "W" in long:
                                long = float(re.findall("[0-9]*\.[0-9]*", long)[0]) * -1
                            else:
                                long = float(re.findall("[0-9]*\.[0-9]*", long)[0])
                            print(lat,long)
                            break
                        else:
                            lat = None
                            long = None
                        # print(name, reactorType, status, location, rup, gec, fgc, id, lat, long)
                    reactors.append(rea.Reactor(name, reactorType, status, location, rup, gec, fgc, id, lat, long))
        return reactors
