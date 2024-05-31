"""
define the url routes of ylqk/api
"""
from django.urls import path

from ylqk.api.meteorological_data import *
from ylqk.api.annoucement import *
from ylqk.api.login import *
from ylqk.api.homepage import *
from ylqk.api.sub_admin import *
from ylqk.api.data_download import *
from utils.auth import TokenRefresh
from ylqk.api.timegpt import *

from django.contrib import admin

urlpatterns = [
    # 用户登录
    path('login', Login.as_view()),
    path('register', Register.as_view()),
    path('retrieve', Retrieve.as_view()),
    path('reset/username', reset_username),
    path('reset/password', reset_password),
    path('refresh', TokenRefresh),

    # 气象数据查询接口
    path("meteorological/station-info", get_station_info),  # 查询所有气象站点信息
    path("meteorological/station-info/all", get_all_station_info),  # 查询指定气象站点信息
    path("meteorological/origin", get_origin_meteorological_data),
    path("meteorological/pressure-data/all", get_all_pressure_data),  # 查询站点气压数据
    path("meteorological/temperature-data/all", get_all_temperature_data),  # 查询站点气温数据
    path("meteorological/humidity-data/all", get_all_humidity_data),  # 查询站点湿度数据
    path("meteorological/wind-data/all", get_all_wind_data),  # 查询站点风力数据
    path("meteorological/cloud-data/all", get_all_cloud_data),  # 查询站点云量数据
    path("meteorological/other-meteorological-data/all", get_all_other_meteorological_data),  # 查询站点其他气象数据
    path("meteorological/update", update_meteorological_data_by_admin),  # 更新站点气象数据
    path("meteorological/interp", get_interp_meteorological_data),  # 查询插值气象数据
    path("meteorological/history", get_history_meteorological_data),  # 查询历史气象数据

    # 数据下载接口
    path("dataservice/upload", file_upload),  # 数据文件上传
    path("dataservice/delete", file_delete),  # 数据文件删除

    # 通知类接口
    path('announcement/unread-number', get_unread_number),  # 获取未读通知数量
    path('announcement/list', get_all_mails),  # 获取所有通知
    path("announcement/id", get_mail_by_id),  # 通过id获取通知详情
    path('announcement/id/admin', tackle_mail_by_id),  # 审核和发布管理员间的通信
    path('announcement/update', get_forecast_from_api),

    # 管理员功能
    path('sub-admin/manual', admin_create_forewarn),  # 手动创建灾害预警

    # 首页其他功能
    path('subscribe-list', get_subscriced_all),  # 获取订阅列表
    path('disasters', get_all_published_disasters),
    path('subscribe', add_subscribe_city),
    path('undo-subscribe', del_subscribe_city),
    path('test', test),

    # AI预测接口
    path("forecast/PRS", get_PRS_forecast),  # 获取气压预测数据
    path("forecast/PRS-Sea", get_PRS_Sea_forecast),  # 获取海平面气压预测数据
    path("forecast/PRS-Max", get_PRS_Max_forecast),  # 获取最高气压预测数据
    path("forecast/PRS-Min", get_PRS_Min_forecast),  # 获取最低气压预测数据
    path("forecast/TEM", get_TEM_forecast),  # 获取气温预测数据
    path("forecast/TEM-MAX", get_TEM_MAX_forecast),  # 获取最高气温预测数据
    path("forecast/TEM-MIN", get_TEM_MIN_forecast),  # 获取最低气温预测数据
    path("forecast/RHU", get_RHU_forecast),  # 获取相对湿度预测数据
    path("forecast/RHU-Min", get_RHU_Min_forecast),  # 获取最小相对湿度预测数据
    path("forecast/VAP", get_VAP_forecast),  # 获取水汽压预测数据
    path("forecast/PRE-3h", get_PRE_3h_forecast),  # 获取3小时降水量预测数据
    path("forecast/WIN-S-MAX", get_WIN_S_MAX_forecast),  # 获取最大风速预测数据
    path("forecast/WIN-S-Inst-Max", get_WIN_S_Inst_Max_forecast),  # 获取极大风速预测数据
    path("forecast/CLO-Cov", get_CLO_Cov_forecast),  # 获取总云量预测数据
    path("forecast/CLO-Cov-Low", get_CLO_Cov_Low_forecast),  # 获取低云量预测数据
]
