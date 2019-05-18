import json
import operator
import math

class TrainLine:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hubs = []
        self.hubLocation = dict()
    def addHubAtKm(self, hub, km):
        self.hubs.append(hub)
        self.hubLocation[hub.name] = km
    def getSortedHubs(self):
        return sorted(self.hubLocation.items(), key=operator.itemgetter(1))

class Hub:

    def __init__(self, name="", x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
    def getCoord(self):
        return self.x, self.y

class SBB:
    def __init__(self):
        self.hubs = dict()
        self.trainLines = dict()

    def importData(self, jsonFileName):
        with open(jsonFileName) as f:
            lines = json.load(f)
        for j in lines:
            if 'fields' not in j:
                continue
            trainLineId = j['fields']['linie']
            if trainLineId not in self.trainLines:
                trainLineName = j['fields']['linienname']
                self.trainLines[trainLineId] = TrainLine(trainLineId, trainLineName)
            hub = Hub()
            hub.name = treatString(j['fields']['bezeichnung_bpk'])
            hub.x = j['fields']['geopos'][1] * 100
            hub.y = j['fields']['geopos'][0] * 100
            km = j['fields']['km']

            self.trainLines[trainLineId].addHubAtKm(hub, km)
            self.hubs[hub.name] = hub

        print('successfully imported ' + str(len(self.hubs)) + ' hubs')
        print('successfully imported ' + str(len(self.trainLines)) + ' train lines')

    def createMap(self):
        map = dict()
        for line in self.trainLines:
            previousHubName = ""
            previousKm = -1
            for h in self.trainLines[line].getSortedHubs():
                hubName = h[0]
                km = h[1]
                if previousHubName:
                    distance = abs(km-previousKm)
                    map.setdefault(hubName,dict())
                    map.setdefault(previousHubName,dict())
                    map[hubName].setdefault(previousHubName)
                    map[previousHubName].setdefault(hubName)
                    map[hubName][previousHubName] = distance
                    map[previousHubName][hubName] = distance
                previousHubName = hubName
                previousKm = km
        return map

    def get_hub_locations(self):
        locations = dict()
        for h in self.hubs:
            locations[h] = self.hubs[h].getCoord()
        return locations
    
    def get_distance_between(self, h1, h2):
        return  math.sqrt((self.hubs[h1].x-self.hubs[h2].x)**2 + (self.hubs[h1].y-self.hubs[h2].y)**2)

def treatString(name):
    name = name.replace(" ", "_")
    name = name.replace('(', "")
    return name.replace(')', "")
