#!/usr/bin/env python

import latlong
from googlemaps import GoogleMaps
from metoffice import MetOffice

def main():
    gmaps = GoogleMaps()
    metoffice = MetOffice()
    test_location = gmaps.postcode_to_latlong("WC1E6BT")
    nearest_id = metoffice.nearest_location_id_to_latlong(test_location)
    print "weather for {0}".format(metoffice.name_of_location_id(nearest_id))
    metoffice.get_forecast_for_location(nearest_id)


if __name__ == '__main__':
    main()
