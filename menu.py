import model
import os
db_file = "nuke.db"
db = model.Database()

#class to make menu

class Menu:
    def __init__(self,data):
        self.data = data

    def main_menu(self):
        os.system('clear')
        for i in range(0, len(self.data)):
            print("{}: {}".format(i+1, self.data[i][0]))

    def selector(self, selec):
        os.system('clear')
        info = db.country_selec(selec)[0]
        print("Country: {}\nNumber of reactors: {}\nCapacity Net-total (MWe): {}\nTotal Generated Electricity (GWh):"
              "{}\nPercent of Total Electricy used: {}%".format(info[1], info[2], info[3], info[4], info[5]))
        return info[1]

    def reactors(self, spec):
        os.system('clear')
        reactors = db.get_reactors_country(spec)
        for i in range(0, len(reactors)):
            name = reactors[i][1]
            type = reactors[i][2]
            status = reactors[i][3]
            city = reactors[i][4]
            rup = reactors[i][5]
            gec = reactors[i][6]
            fcg = reactors[i][7]
            print("Name: {}\nType: {}\nStatus: {}\nCity: {}\nReference Unit Power  [MW]: {}\nGross Electrical Capacity "
                  "[MW]: {}\nFirst Grid Connection: {}\n--".format(name, type, status, city, rup, gec, fcg))
