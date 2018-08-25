import requests
from bs4 import BeautifulSoup
from lxml import html
import pdb
import re
import logging
import datetime
import time

class Planet:
    # planet's current location prediction could be scattered throughout the sky. What is (maxRa, maxDec) (in arc seconds) until we discard the planet
    maxScatteredness = (5000, 5000)
    # Warn when object is scattered (but don't flag it as discarded)
    maxScatterednessWarning = (1000, 1000)
    # Min score for planet to be worth observing
    minScore = 80
    # Min Magnitude
    minMagnitude = 22

    def __init__(self, info):
        parts = info.split()
        self.name = parts[0]
        self.score = int(parts[1])
        # Rectacension
        self.ra = float(parts[5])
        # Declination
        self.dec = float(parts[6])
        self.magnitude = float(parts[7])
        # Object not good for observing
        self.discard = False

        print("\nWorking on: " + self.name)

        self.scatterednessUrl = False
        self.getEphemerides()

        if self.haveWeObserved():
            self.discard = True
            logger.warning('Planet ' + self.name + ' discarded. Reason: we have observed it already before')

        if self.score < Planet.minScore:
            self.discard = True
            logger.warning('Planet ' + self.name + ' discarded. Reason: score too low (' + str(self.score) + ')')

        if self.scatterednessUrl:
            scat = self.getScatteredness()

            if scat[0] > Planet.maxScatteredness[0] or scat[1] > Planet.maxScatteredness[1]:
                self.discard = True
                logger.warning('Planet ' + self.name + ' discarded. Reason: predicted locations too scattered (' + str(scat[0]) + ', ' + str(scat[1]) + ')')
            elif scat[0] > Planet.maxScatterednessWarning[0] or scat[1] > Planet.maxScatterednessWarning[1]:
                logger.warning('Location of planet ' + self.name + ' is very scattered! (' + str(scat[0]) + ', ' + str(scat[1]) + ')')
            # pdb.set_trace()

        # TODO: filter not seen > 1.2 days (and added)

        # Get Max Altitude
        # TODO - do something with maximum altitude
        if len(self.ephemerides) > 0:
            self.maxAltitudeEphemeride = self.maxAlt()
            if self.maxAltitudeEphemeride:
                pass
                # print("Max Altitude Date: " + self.maxAltitudeEphemeride.date)
                if self.maxAltitudeEphemeride.effMagnitude > Planet.minMagnitude:
                    self.discard = True
                    logger.warning('Planet ' + self.name + ' discarded. Reason: effective magnitude too low (' + str(self.maxAltitudeEphemeride.magnitude) + ')')
            else:
                self.discard = True
                logger.warning('Planet ' + self.name + ' discarded. Reason: no maximum altitude obtained')
        else:
            self.discard = True
            logger.warning('Planet ' + self.name + ' discarded. Reason: no ephemerides available')

        

        if not self.discard:
            logger.warning('PLANET OK: ' + self.name)


    def getEphemerides(self):
        url = "https://cgi.minorplanetcenter.net/cgi-bin/confirmeph2.cgi"
        # print(self.name)
        req = requests.post(url, data={"mb": -30, "mf": 30, "dl": -90, "du": +90, "nl": 0, "nu": 100, "sort": "d", "W": "j", "obj": self.name, "Parallax": 1, "obscode": "L01", "long": None, "lat": None, "alt": None, "int": 1, "start": 0, "raty": "a", "mot": "m", "dmot": "p", "out": "f", "sun": "x", "oalt": 20})
        resp = req.text
        page = BeautifulSoup(resp, "html5lib")
        links = page.find("pre")
        lines = (links.text).split("\n")
        lines = lines[2:-1]
        lines = [l for l in lines if "<suppressed>" not in l]

        # if html.find("pre").find_all('a')[2]['href']
        if len(page.find("pre").find_all('a')) > 1 and page.find("pre").find_all('a')[1]['href']:
            self.scatterednessUrl = page.find("pre").find_all('a')[1]['href']

        tree = html.fromstring(req.content)
        if len(tree.xpath("//a[text()='observations']/@href")) > 0:
            self.observationsUrl = tree.xpath("//a[text()='observations']/@href")[0]

        self.ephemerides = []
        for l in lines:
            eph = Ephemeride(l)
            if eph.isValid():
                self.ephemerides.append(eph)

    def maxAlt(self):
        maxAlt = float("-inf")
        index = None

        # logger.warning('Obtaining efemeride for: ' + self.name)
        for i, eph in enumerate(self.ephemerides):
            # logger.warning('Eph.alt: ' + str(eph.alt))
            if eph.alt > maxAlt:
                maxAlt = eph.alt
                index = i
        if index is None:
            self.discard = True
            return None
        return self.ephemerides[index]

    # Have we observed the planet before
    def haveWeObserved(self):
        resp = requests.get(self.observationsUrl)
        tree = html.fromstring(resp.content)
        text = tree.xpath('//pre/text()')
        # pdb.set_trace()
        if re.search("L01\n", text[0]):
            return True
        return False


    # scatteredness of results
    def getScatteredness(self):
        req = requests.get(self.scatterednessUrl)
        resp = req.text
        html = BeautifulSoup(resp, "html5lib")
        links = html.find("pre")

        observationPoints = re.findall('([+-][0-9]+) +([+-][0-9]+)', links.text)
        minRa, maxRa, minDec, maxDec = 0, 0, 0, 0
        for point in observationPoints:
            if int(point[0]) < minRa:
                minRa = int(point[0])
            elif int(point[0]) > maxRa:
                maxRa = int(point[0])
            if int(point[1]) < minDec:
                minDec = int(point[1])
            elif int(point[1]) > maxDec:
                maxDec = int(point[1])

        return (maxRa - minRa, maxDec - minDec)

# planet1 = Planet()


class Ephemeride:
    # Maximum sun altiude (otherwise we can't observe the planet)
    maxSunAlt = -15

    def __init__(self, info):
        self.line = info
        parts = self.line.split()
        self.date = parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' ' + parts[3]
        self.dateUnix = time.mktime(datetime.datetime.strptime(self.date, "%Y %m %d %H%M").timetuple())
        # Altitude of object (above horizon) at that time
        self.alt = float(parts[15])
        # Altitude of sun at the time
        self.sunAlt = float(parts[16])
        self.magnitude = float(parts[11])
        # Effective magnitude - Manitude that takes into account atmospheric extiction due to (low) altitude of planet
        self.effMagnitude = self.getEffectiveMagnitude()
        # Observation time needed (in minutes) - approximates the imaging time needed to get a good picture
        self.observationTime = self.getObservationTime()
        # pdb.set_trace()
        # logger.warning('Magnitude vs Effective Magnitude: ' + str(self.magnitude) + " : " + str(self.effMagnitude))


    def isValid(self):
        if self.sunAlt < Ephemeride.maxSunAlt:
            return True
        return False

    def getEffectiveMagnitude(self):
        return self.magnitude + ((self.alt - 40) * 0.1)

    def getObservationTime(self):
        return round(10 + (self.effMagnitude - 18) * 5, 2)


class Main:
    def __init__(self):
        self.planets = self.getData()
        self.writeToFile()

    def getData(self):
        url = "https://www.minorplanetcenter.net/iau/NEO/neocp.txt"
        req = requests.get(url).text[:-1].split("\n")
        planets = []
        for planetString in req:
            p = Planet(planetString)
            # TODO: check if planet is OK or discard otherwise
            planets.append(p)

        return planets

    def sortByMaxAlt(self):
        return sorted([p for p in self.planets if not p.discard], key=lambda planet: planet.maxAltitudeEphemeride.dateUnix)


    def writeToFile(self):
        logger.warning('Writing output to file')

        # pdb.set_trace()

        with open(datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-planets", "w") as f:
            header = """Date       UT   *  R.A. (J2000) Decl.  Elong.  V        Motion     Object     Sun         Moon
                       h m                                      "/min   P.A.  Azi. Alt.  Alt.  Phase Dist. Alt."""+"\n\n\n"
            f.write(header + "\n")
            sortedPlanets = self.sortByMaxAlt()
            for p in sortedPlanets:
                if not p.discard:
                    f.write("* " + p.name + "         score=" + str(p.score) + ", observationTime=" + str(p.maxAltitudeEphemeride.observationTime) + "\n")
                    f.write(p.maxAltitudeEphemeride.line + "\n\n")
            f.close()

logger = logging.getLogger()
planets = Main()
# pdb.set_trace()