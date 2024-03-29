import httplib
import urllib
from latlong import LatLong
import xml.dom.minidom
import dateutil.parser

weather_types = ['Clear night', 'Sunny day', 'Partly cloudy (night)',
                  'Partly cloudy (day)', 'Not used', 'Mist', 'Fog', 
                  'Cloudy', 'Overcast', 'Light rain shower (night)', 
                  'Light rain shower (day)', 'Drizzle', 'Light rain',
                  'Heavy rain shower (night)', 'Heavy rain shower (day)', 
                  'Heavy rain', 'Sleet shower (night)', 'Sleet shower (day)',
                  'Sleet', 'Hail shower (night)', 'Hail shower (day)',
                  'Hail', 'Light snow shower (night)', 'Light snow shower (day)',
                  'Light snow', 'Heavy snow shower (night)', 'Heavy snow shower (day)',
                  'Heavy snow', 'Thunder shower (night)', 'Thunder shower (day)',
                  'Thunder']

class MetOffice:
    def __init__(self, api_key):
        self.api_key = api_key 
        self.base_url = "datapoint.metoffice.gov.uk"
        self.locations = None


    def name_of_location_id(self, loc_id):
        return self.locations[loc_id][0]


    def nearest_location_id_to_latlong(self, target_location):
        if self.locations == None:
            self.get_locations_table()
        nearest_location_id = ""
        shortest_distance = float('Inf')
        for loc_id, loc_details in self.locations.iteritems():
            dist = target_location.distance(loc_details[1])
            if dist < shortest_distance:
                nearest_location_id = loc_id
                shortest_distance = dist
        return nearest_location_id


    def get_locations_table(self):
        query = {'key' : self.api_key}
        connection = httplib.HTTPConnection(self.base_url)
        connection.request("GET", "/public/data/val/wxfcs/all/xml/sitelist?" + urllib.urlencode(query))
        response = connection.getresponse()
        raw_data = response.read()
        connection.close()
        xml_data = xml.dom.minidom.parseString(raw_data)
        self.locations = {}
        for location in xml_data.getElementsByTagName("Location"):
            loc_id = location.getAttribute("id")
            loc_lat = float(location.getAttribute("latitude"))
            loc_long = float(location.getAttribute("longitude"))
            position = LatLong(loc_lat, loc_long)
            loc_name = location.getAttribute("name")
            self.locations[loc_id] = (loc_name, position)


    def get_forecast_for_location(self, location):
        query = {'key': self.api_key, 'res': '3hourly'}
        connection = httplib.HTTPConnection(self.base_url)
        request_path = "/public/data/val/wxfcs/all/xml/{0}?".format(location)
        connection.request("GET", request_path + urllib.urlencode(query))
        response = connection.getresponse()
        raw_data = response.read()
        connection.close()
        xml_data = xml.dom.minidom.parseString(raw_data)
        for day in xml_data.getElementsByTagName("Period"):
            ForecastDay(day)


class ForecastDay:
    def __init__(self, xml_forecast):
        self.date = dateutil.parser.parse(xml_forecast.getAttribute("value"), fuzzy=True)
        self.forecasts = []
        for rep in xml_forecast.getElementsByTagName("Rep"):
            self.forecasts.append(SingleForecast(self.date, rep))
        for fc in self.forecasts:
            print fc.forecast_as_text()


class SingleForecast:
    def __init__(self, day, xml_forecast):
        self.datetime = day + dateutil.relativedelta.relativedelta(minutes=int(xml_forecast.firstChild.data))
        self.wind_direction = xml_forecast.getAttribute("D")
        self.feels_like_temp = int(xml_forecast.getAttribute("F"))
        self.wind_gusts = int(xml_forecast.getAttribute("G"))
        self.humidity = int(xml_forecast.getAttribute("H"))
        self.percipitation_probability = int(xml_forecast.getAttribute("Pp"))
        self.wind_speed = int(xml_forecast.getAttribute("S"))
        self.max_uv_index = int(xml_forecast.getAttribute("U"))
        self.weather_type = weather_types[int(xml_forecast.getAttribute("W"))]
        self.temperature = int(xml_forecast.getAttribute("T"))

    def forecast_as_text(self):
        return "{0}: Wind {1} at {2} kts (gusting: {3} kts). {4}% prob. of percipitation".format(self.datetime, self.wind_direction, self.wind_speed, self.wind_gusts, self.percipitation_probability)
