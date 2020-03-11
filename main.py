import model
import menu

db_file = "nuke.db"

params = {
  'dbname': 'nuke',
  'user': 'tony',
  'password': 'rOflstomp11!',
  'host': '18.216.34.118',
  'port': 5432
}
db = model.Database()
data = db.load_countries()
disp = menu.Menu(data)


def main():
    startup()
    breaker = 0
    while breaker == 0:
        disp.main_menu()
        selec = input("Select a country: ")
        spec = disp.selector(selec)
        specifics = input("More Info?: ")
        if specifics.upper() == "Y":
            disp.reactors(spec)
        cont = input("Continue?: ")
        if cont is "y":
            disp.main_menu()
        else:
            breaker = 1

def startup():
    if db.table_check('nuke_countries') is False:
        db.insert_countries()
    if db.table_check('nuke_reactors') is False:
        db.insert_reactors()


if __name__ == '__main__':
    main()