import json

import requests
from django.utils import timezone
import pytz
from datetime import datetime
from ylqk.models.announcement import AIDisasterForecast
from apscheduler.schedulers.background import BackgroundScheduler

def get_period_forecast():
    url = "https://api.seniverse.com/v3/weather/alarm.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/117.0.0.0'
    }
    param = {
        'key' : 'S7im19ViaQ4UkF7t9', # 私钥！！！
        'detail' : 'more',
    }
    response = requests.get(url = url,params = param,headers=headers)
    data = response.json()
    for item in data['results']:
        loc = item['location']['path']
        locs = loc.split(',')
        num = len(locs)
        province = locs[num - 2] if num >= 2 else ""
        city = locs[num - 3] if num >= 3 else ""
        district = locs[num - 4] if num >= 4 else ""
        location = province + "-" + city + "-" + district
        for forecast in item['alarms']:
            alarm_id = forecast['alarm_id']
            dis = AIDisasterForecast.objects.filter(alarm_id=alarm_id).first()
            if dis is None:  #
                disaster = AIDisasterForecast.objects.create(disaster_type="-1", disaster_level=-1,
                                                             disaster_location="-1", disaster_longitude=-1,
                                                             disaster_latitude=-1)
                disaster.disaster_location = location
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
