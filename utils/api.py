import json

import requests
from django.utils import timezone
import pytz
from datetime import datetime
from ylqk.models.announcement import AIDisasterForecast
from apscheduler.schedulers.background import BackgroundScheduler
from ylqk.api.sub_admin import get_location_by_address

def get_period_forecast():
    url = "https://api.seniverse.com/v3/weather/alarm.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/117.0.0.0'
    }
    param = {
        'key' : 'SN_H868TafuTTtyLb', # 私钥！！！
        'detail' : 'more',
    }
    response = requests.get(url = url,params = param,headers=headers)
    data = response.json()
    for item in data['results']:
        loc = item['location']['path']
        locs = loc.split(',')
        num = len(locs)
        if num == 3: # 直辖市
            province = locs[1]
            city = locs[1]
            district = locs[0]
        if num == 4: # 省 or 自治区
            province = locs[2]
            city = locs[1]
            district = locs[0]
        location = province + "-" + city + "-" + ("" if city==district else district)
        for forecast in item['alarms']:
            alarm_id = forecast['alarm_id']
            dis = AIDisasterForecast.objects.filter(alarm_id=alarm_id).first()
            if dis is None:  #
                disaster = AIDisasterForecast.objects.create(disaster_type="-1", disaster_level=-1,
                                                             disaster_location="-1", disaster_longitude=-1,
                                                             disaster_latitude=-1)
                disaster.disaster_location = location
                addr = get_location_by_address(location)
                disaster.disaster_latitude = addr['lat']
                disaster.disaster_longitude = addr['lng']
                disaster.disaster_type = forecast['type']
                disaster.disaster_level = forecast['level']
                disaster.disaster_description = forecast['description']
                aware_datetime = datetime.strptime(forecast['pub_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
                aware_datetime = aware_datetime.astimezone(pytz.timezone('Asia/Shanghai'))
                disaster.datatime = aware_datetime
                disaster.alarm_id = alarm_id
                disaster.save()
                from ylqk.api.annoucement import publish
                publish(disaster.id)
            else:  # 灾害的修改要重新通知还是要忽略？
                pass
