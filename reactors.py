class Reactor():
    def __init__(self, name, reactorType, status, location, rup, gec, fgc, countryCode):
        self.name = name
        self.reactorType = reactorType
        self.status = status
        self.location = location
        self.rup = rup
        self.gec = gec
        self.fgc = fgc
        self.countryCode = countryCode

    def getName(self):
        if self.name is None:
            self.name = 'Null'
        return self.name

    def getType(self):
        if self.reactorType is None:
            self.reactorType = 'Null'
        return self.reactorType

    def getStatus(self):
        if self.status is None:
            self.status = 'Null'
        return self.status

    def getLocation(self):
        if self.location is None:
            self.location = 'Null'
        return self.location

    def getRup(self):
        if self.rup is None:
            self.rup = 'Null'
        return self.rup

    def getGec(self):
        if self.gec is None:
            self.gec = 'Null'
        return self.gec

    def getFgc(self):
        if self.fgc is None:
            self.fgc = 'Null'
        return self.fgc

    def getcountryCode(self):
        return self.countryCode