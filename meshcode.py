import math

class IntegralPartParser:

    def parse(self, remLat, remLon):
        remLat /= 3600
        remLon /= 3600
        lon1st = int(math.floor(remLon-100))
        lat1st = int(math.floor(remLat*1.5))
        return {
            'remLat': 3600 * (remLat - lat1st/1.5),
            'remLon': 3600 * (remLon - (lon1st+100)),
            'code': "%02d%02d" % (lat1st, lon1st)
        }

    def unit(self):
        return ( 3600 * 2.0/3, 3600 * 1.0 )

    def invert(self, code):
        latCode = code[0:2]
        lonCode = code[2:4]
        return {
            'code': code[4:],
            'lat': int(latCode) * 2.0/3 * 3600,
            'lon': (100 + int(lonCode)) * 3600
        }

class DecimalPartParser:

    def __init__(self, latUnit, lonUnit, offset=0, radix=10, digits=2):
        self.latUnit = latUnit
        self.lonUnit = lonUnit
        self.offset = offset
        self.radix = radix
        self.digits = digits

    def parse(self, remLat, remLon):
        roundedRemLat = round( remLat, 4 )
        roundedRemLon = round( remLon, 4 )
        lat2nd = int(math.floor(roundedRemLat/self.latUnit))
        lon2nd = int(math.floor(roundedRemLon/self.lonUnit))
        return {
            'remLat': remLat - lat2nd * self.latUnit,
            'remLon': remLon - lon2nd * self.lonUnit,
            'code': "{1:0{0}d}".format(self.digits, lat2nd * self.radix + lon2nd + self.offset)
        }

    def unit(self):
        return ( self.latUnit, self.lonUnit )

    def invert( self, code ):
        _code = int(code[0:self.digits]) - self.offset
        return {
            'code': code[self.digits:],
            'lat': int(_code / self.radix) * self.unit()[0],
            'lon': int(_code % self.radix) * self.unit()[1]
        }

class _Level:

    parsers = []

    def __init__(self, *parsers):
        if _Level == type(parsers[0]):
            self.parsers = parsers[0].parsers
            self.parsers += parsers[1:]
        else:
            self.parsers = parsers

class Level:

    L1 = _Level(
        IntegralPartParser()
    )
    L2 = _Level(
        L1,
        DecimalPartParser(300, 450)
    )
    L3 = _Level(
        L2,
        DecimalPartParser(30, 45)
    )
    HALF = _Level(
        L3,
        DecimalPartParser(15, 22.5, radix=2, offset=1, digits=1)
    )
    QUOTER = _Level(
        HALF,
        DecimalPartParser(7.5, 11.25, radix=2, offset=1, digits=1)
    )
    EIGHTH = _Level(
        QUOTER,
        DecimalPartParser(3.75, 5.625, radix=2, offset=1, digits=1)
    )
    TWENTYTH = _Level(
        HALF,
        DecimalPartParser(1.5, 2.25)
    )

def code( lat, lon, level ):
    codes = []
    remLat = lat * 3600
    remLon = lon * 3600
    for f in level.parsers:
        r = f.parse( remLat, remLon )
        remLat = r['remLat']
        remLon = r['remLon']
        codes.append(r['code'])
        
    return "".join(codes)

def polygon(code, level):
    base = basePointFromCode( code, level )
    f = level.parsers[-1]
    left = base[0]
    bottom = base[1]
    right = left + f.unit()[1]/3600
    top = bottom + f.unit()[0]/3600
    return (
        (left, bottom),
        (left, top),
        (right, top),
        (right, bottom)
    )

def basePointFromCode(code, level):
    lat = 0
    lon = 0
    for f in level.parsers:
        r = f.invert(code)
        code = r['code']
        lat += r['lat']
        lon += r['lon']
        
    return (lon/3600, lat/3600)
