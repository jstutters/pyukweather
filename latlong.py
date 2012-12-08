import math

class LatLong:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance(self, other):
        R = 6371.0 # kilometres
        dlat = math.radians(other.latitude - self.latitude)
        dlong = math.radians(other.longitude - self.longitude)
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        h = haversin(dlat) + (math.cos(lat1) * math.cos(lat2) * haversin(dlong))
        d = 2.0 * R * math.asin(math.sqrt(h))
        return d

def haversin(theta):
    return (1.0 - math.cos(theta)) / 2.0
