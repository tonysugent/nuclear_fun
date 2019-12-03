import sqlite3
from scraper import Scraper

# initialize a scraper object to use

s = Scraper()


class Database:
    def __init__(self, db):
        self.db = db
        self.c = sqlite3.connect(self.db)
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
            self.cursor.execute(
                '''INSERT INTO countries(id,'country',reactors,capacity_total,generated_electricity,percent_use,country_code)
                 values({}, '{}', '{}', '{}', '{}', '{}', '{}');'''.format(id, country, reactors, capacity_total,
                                                                                      generated_electricity, percent_use, country_code))
            self.c.commit()

    def load_countries(self):
        # loads countries for main menu
        data = self.c.execute('''SELECT country from countries''').fetchall()
        return data

    def table_check(self, table_name):
        # check to see if table is populated
        # referenced in the start up functions
        check = self.c.execute('''SELECT count(*) from {}'''.format(table_name)).fetchall()
        if check[0][0] != 0:
            return True
        else:
            return False

    def country_selec(self, selec):
        choice = self.c.execute('''SELECT * from countries where id = {};'''.format(int(selec)-1)).fetchall()
        print(choice)
        return choice

    def get_country_codes(self):
        #grab country code and id from country table
        codes = self.cursor.execute('''SELECT country_code,id from countries''').fetchall()
        return codes

    def insert_reactors(self):
        # insert reactor data into database
        data = s.get_reactors()

        for i in range(0, len(data)):
            self.cursor.execute('''INSERT INTO reactors(id,name,type,status,city,rup,gec,fgc) values({},"{}",'{}',
            '{}',"{}",{},{},{})'''.format(data[i].getcountryCode(), data[i].getName(), data[i].getType(), data[i].getStatus(),
                                  data[i].getLocation(), data[i].getRup(), data[i].getGec(), data[i].getFgc()))
            self.c.commit()

    def get_reactors(self):
        # get all nuclear reactors.. probably going to use this for stats later
        self.cursor.execute('''select * from reactors''')

    def get_reactors_country(self, country):
        # get reactors based on country
        countryId = self.cursor.execute('''select id from countries where country like "{}"'''.format(country)).fetchone()
        reactors = self.cursor.execute('''select * from reactors where id = {}'''.format(countryId[0])).fetchall()
        return reactors
