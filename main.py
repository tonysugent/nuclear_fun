import model
import menu

db_file = "nuke.db"
db = model.Database(db_file)
data = db.load_countries()
disp = menu.Menu(data)


def main():
    startup()
    disp.main_menu()
    selec = input("Select a country: ")
    spec = disp.selector(selec)
    specifics = input("More Info?: ")
    if specifics.upper() == "Y":
        disp.reactors(spec)


def startup():
    if db.table_check('countries') is False:
        db.insert_countries()
    if db.table_check('reactors') is False:
        db.insert_reactors()


if __name__ == '__main__':
    main()