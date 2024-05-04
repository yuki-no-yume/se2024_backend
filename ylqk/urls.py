"""
define the url routes of ylqk/api
"""
from django.urls import path

from ylqk.api.meteorological_data import *
from ylqk.api.annoucement import *
from ylqk.api.login import *
from ylqk.api.homepage import *
from ylqk.api.sub_admin import *

from django.contrib import admin

urlpatterns = [
    # 用户登录
    path('login/', Login.as_view()),
    path('register', Register.as_view()),

    # 气象数据查询接口
    path("meteorological/station-info", get_station_info),  # 查询单个站点信息
    path("meteorological/station-info/all", get_all_station_info),  # 查询所有站点信息
    path("meteorological/pressure-data/all", get_all_pressure_data),    # 查询所有气压数据
    path("meteorological/temperature-data/all", get_all_temperature_data),  # 查询所有温度数据
    path("meteorological/humidity-data/all", get_all_humidity_data),    # 查询所有湿度数据
    path("meteorological/wind-data/all", get_all_wind_data),    # 查询所有风力数据
    path("meteorological/cloud-data/all", get_all_cloud_data),  # 查询所有云量数据
    path("meteorological/other-meteorological-data/all", get_all_other_meteorological_data),    #查询其他气象数据
    path('meteorological/update', update_meteorological_data_by_admin),  # 管理员手动更新气象数据

    # 通知类接口
    path("announcement/admin/disaster", get_admins_all),  # 模型审批通知
    path("announcement/user/suscribed", get_users_all),  # 订阅灾害通知
    path("announcement/admin/user", get_private_all),  # 管理员身份审批通知
    path("announcement/system", get_system_all),  # 系统通知
    path("announcement/id", get_mail_by_id),  # 通过id获取通知
    path('announcement/id/admin', tackle_mail_by_id),  # 管理员通过id审批通知

    # 首页其他功能
    path('suscribe-list', get_subscriced_all),  # 获取订阅列表
    path('upgrade', submit_more_info),  # 申请成为管理员
    path('disasters', get_all_published_disasters),

    # 管理员功能
    # path('sub-admin/ban',), # 禁言用户
    # path('sub-admin/unban',), # 取消用户禁言
    path('sub-admin/manual', create_forewarn),  # 手动创建灾害预警
    path('sub-admin/modify', modify_forewarn),  # 删除灾害预警
]
