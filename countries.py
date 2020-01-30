class Country:
    def __init__(self, country, reactors, capacity_total,generated_electricity, percent_use, country_code):
        self.country = country
        self.reactors = reactors
        self.capacity_total = capacity_total
        self.generated_electricity = generated_electricity
        self.percent_use = percent_use
        self.country_code = country_code

    def getCountry(self):
        if self.country is None:
            return 'Null'
        return self.country

    def getReactors(self):
        if self.reactors is None:
            return 'Null'
        return self.reactors

    def getCapacityTotal(self):
        if self.capacity_total is None:
            return 'Null'
        return float(self.capacity_total.split(" ")[0].replace(",", ""))

    def getGenerated(self):
        if self.generated_electricity is None:
            return 'Null'
        return self.generated_electricity.split(" ")[0].replace(",", "")

    def getPercentUse(self):
        if self.percent_use is None:
            return 'Null'
        return float(self.percent_use.replace("%", ""))

    def getCountryCode(self):
        if self.country_code is None:
            return 'Null'
        else:
             self.country_code = "'" + self.country_code +"'"
        return self.country_code




#id, country, reactors, capacity_total,generated_electricity, percent_use, country_code