"""
define the url routes of ylqk/api
"""
from django.urls import path

from ylqk.api.meteorological_data import get_station_info, get_all_station_info, get_all_pressure_data

urlpatterns = [
    path("meteorological/station-info", get_station_info),
    path("meteorological/station-info/all", get_all_station_info),
    path("meteorological/pressure-data/all", get_all_pressure_data),
]
