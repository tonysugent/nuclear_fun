import sqlite3
from scraper import Scraper
import psycopg2
# initialize a scraper object to use

s = Scraper()


class Database:
    def __init__(self):

        self.c = psycopg2.connect(database='nuke',user='postgres',password='rOflstomp11!', host='18.219.19.27',port=5432)
        self.cursor = self.c.cursor()

    def insert_countries(self):
        data = s.country_data()
        # insert data on countries from web scraping class. todo make country class
        for i in range(0, len(data)):
            print(data[i])
            id = i
            country = data[i].getCountry()
            reactors = data[i].getReactors()
            capacity_total = data[i].getCapacityTotal()
            generated_electricity = data[i].getGenerated()
            percent_use = data[i].getPercentUse()
            country_code = data[i].getCountryCode()
            print("""INSERT INTO nuke_countries(id,country,reactors,capacity_total,generated_electricity,percent_use,country_code)
                 values({}, '{}', '{}', {}, {}, {}, {});""".format(id, country, reactors, capacity_total,
                                                                   generated_electricity, percent_use, country_code))
            self.cursor.execute(
                """INSERT INTO nuke_countries(id,country,reactors,capacity_total,generated_electricity,percent_use,country_code)
                 values({}, '{}', '{}', {}, {}, {}, {});""".format(id, country, reactors, capacity_total,
                                                                   generated_electricity, percent_use, country_code))
            self.c.commit()

    def load_countries(self):
        # loads countries for main menu
        self.cursor.execute('''SELECT country from nuke_countries''')
        data = self.cursor.fetchall()
        return data

    def table_check(self, table_name):
        # check to see if table is populated
        # referenced in the start up functions
        self.cursor.execute('''SELECT count(*) from {}'''.format(table_name))
        check = self.cursor.fetchone()
        print(check[0])
        if check[0] != 0:
            return True
        else:
            return False

    def country_selec(self, selec):
        self.cursor.execute('''SELECT id,country,reactors,capacity_total,generated_electricity,percent_use,
        country_code from nuke_countries where id = {};'''.format(int(selec)-1))
        choice = self.cursor.fetchall()
        print(choice)
        return choice

    def get_country_codes(self):
        #grab country code and id from country table
        self.cursor.execute('''SELECT country_code,id from nuke_countries''')
        codes = self.cursor.fetchall()
        return codes

    def insert_reactors(self):
        # insert reactor data into database
        data = s.get_reactors()

        for i in range(0, len(data)):
            self.cursor.execute('''INSERT INTO nuke_reactors(id,name,type,status,city,rup,gec,fgc) values({},'{}','{}',
            '{}','{}',{},{},{})'''.format(data[i].getcountryCode(), data[i].getName(), data[i].getType(), data[i].getStatus(),
                                  data[i].getLocation(), data[i].getRup(), data[i].getGec(), data[i].getFgc()))
            self.c.commit()

    def get_reactors(self):
        # get all nuclear reactors.. probably going to use this for stats later
        self.cursor.execute('''select id,name,type,status,city,rup,gec,fgc from nuke_reactors''')

    def get_reactors_country(self, country):
        # get reactors based on country
        print(country)
        self.cursor.execute('''select id from nuke_countries where country ilike '{}' '''.format(country))
        countryId = self.cursor.fetchone()
        self.cursor.execute('''select id,name,type,status,city,rup,gec,fgc  from nuke_reactors where id = {}'''.format(countryId[0]))
        reactors = self.cursor.fetchall()
        return reactors
