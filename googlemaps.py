import httplib
import urllib
import latlong

class GoogleMaps:
    def __init__(self):
        self.api_key = "ABQIAAAATkxdaUg_lM5H_9FIVKUGJxTdZhKW-pBFDOhTyke-p5n9FagHohSaxydxqsrt8iiuh5-zAhiQLmc5sQ"
        self.base_url = "maps.google.co.uk"


    def postcode_to_latlong(self, postcode):
        query = {'output' : 'csv', 'q' : postcode, 'key' : self.api_key}
        connection = httplib.HTTPConnection(self.base_url)
        connection.request("GET", "/maps/geo?" + urllib.urlencode(query))
        response = connection.getresponse()
        data = response.read()
        connection.close()
        items = data.split(',')
        if len(items) == 4:
            return latlong.LatLong(float(items[2]), float(items[3]))
        else:
            return None
