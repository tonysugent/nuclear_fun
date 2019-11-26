import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import model
import reactors as re

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

        for i in jsondata:
            for j in code_data:
                if i['Country'] == j['COUNTRY']:
                    i['country_code'] = j['ISO CODES']

        return jsondata

    def get_reactors(self):
        db_file = "nuke.db"
        db = model.Database(db_file)
        con = db.get_country_codes()
        dict = {}
        reactors =[]
        for i in range(0, len(con)):
            url = 'https://pris.iaea.org/PRIS/CountryStatistics/CountryDetails.aspx?current=' + con[i][0].replace(" ",
                                                                                                                  "")
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            table = soup.find_all('table')
            df = pd.read_html(str(table), header=0)
            jsondata = json.loads(df[3].to_json(orient='index'))
            dict[con[i][0].replace(" ", "")] = jsondata


        # manipulate json data and add country id to the reactors from the countries table
        for i in range(0,len(con)):
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
                reactors.append(re.Reactor(name, reactorType, status, location, rup, gec, fgc, id))
                print(dict[con[i][0].replace(" ", "")][str(j)])
        return reactors



