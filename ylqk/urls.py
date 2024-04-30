"""
define the url routes of ylqk/api
"""
from django.urls import path

from ylqk.api.meteorological_data import *
from ylqk.api.annoucement import *
from ylqk.api.login import *

from django.contrib import admin

urlpatterns = [
    #用户登录
    path('login/',Login.as_view),

    # 气象数据查询接口
    path("meteorological/station-info", get_station_info),
    path("meteorological/station-info/all", get_all_station_info),
    path("meteorological/pressure-data/all", get_all_pressure_data),
    path("meteorological/temperature-data/all", get_all_temperature_data),
    path("meteorological/humidity-data/all", get_all_humidity_data),
    path("meteorological/wind-data/all", get_all_wind_data),
    path("meteorological/cloud-data/all", get_all_cloud_data),
    path("meteorological/other-meteorological-data/all", get_all_other_meteorological_data),

    #通知类接口
    path("announcement/admin",get_admins_all),
    path("announcement/user",get_users_all),
    path("announcement/system",get_system_all),
    path("announcement/id",get_mail_by_id),
]
