import requests
import pandas as pd
from nixtla import NixtlaClient
import matplotlib.pyplot as plt
from django.views.decorators.http import require_GET, require_POST
import requests
import numpy as npy
import geopandas as gpd
from django.http import HttpRequest
from datetime import datetime, timedelta
from scipy import interpolate
from shapely.geometry import Point

from utils.api_key import *
from utils.response_util import *
from ylqk.models.interp_data import *
from ylqk.models.meteorological_data import *
from csv import *

nixtla_client = NixtlaClient(
    api_key='nixtla-tok-8H9udQiTNLFccVt4zna5elR6NeLZlVewB8bbrkto9LduI54vigOv6URGGpROq3ziMkKNboShVw2fmwtj'
)


# Read the data
# Read data

# df = pd.read_csv('data.csv')


def addZero(line):
    if (str.__len__(line) == 1):
        return '0' + line
    else:
        return line


# Load the future value of exogenous variables over the forecast horizon
# future_ex_vars_df = pd.read_csv('D:/B_6/软工/表格/t8.csv')

# future_ex_vars_df = pd.read_csv('https://raw.githubusercontent.com/Nixtla/transfer-learning-time-series/main/datasets/electricity-short-future-ex-vars.csv')
# df = pd.read_csv('https://raw.githubusercontent.com/Nixtla/transfer-learning-time-series/main/datasets/electricity-short-with-ex-vars.csv')


@require_GET
def get_PRS_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []
    for info in data['DS']:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    # timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS_Sea['ds'],
        # 'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_PRS_Sea_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    # timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        # 'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_PRS_Max_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    # timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        # 'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_PRS_Min_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    # timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        # 'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_TEM_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    # timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        # 'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_TEM_MAX_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    # timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        # 'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_TEM_MIN_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    # timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        # 'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_RHU_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    # timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        # 'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_RHU_Min_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    # timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        # 'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_VAP_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    # timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        # 'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_PRE_3h_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    # timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        # 'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_WIN_S_MAX_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    # timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        # 'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_WIN_S_Inst_Max_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    # timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h', target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        # 'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_CLO_Cov_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    # timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        # 'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


@require_GET
def get_CLO_Cov_Low_forecast(request: HttpRequest):
    end = datetime.now()
    delta = timedelta(days=5)
    begin = end - delta
    end = end.strftime('%Y%m%d%H%M%S')
    begin = begin.strftime('%Y%m%d%H%M%S')
    time = '[' + begin + ',' + end + ']'
    account = '716993315790upwVr'
    password = 'GxSThLx'
    staId = request.GET.get("station_id")
    response = requests.get(
        'http://api.data.cma.cn:8090/api?userId=' + account + '&pwd=' + password + '&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H&timeRange=' + time + '&staIDs=' + staId + '&elements=Station_Id_C,Year,Mon,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,TEM,TEM_MAX,TEM_MIN,RHU,RHU_Min,VAP,PRE_3h,WIN_S_MAX,WIN_S_Inst_Max,CLO_Cov,CLO_Cov_Low')
    data = response.json()
    infos = []

    for info in data:
        element = {
            'Station_Id_C': info['Station_Id_C'],
            'ds': info['Year'] + '-' + addZero(info['Mon']) + '-' + addZero(info['Day']) + ' ' + addZero(
                info['Hour']) + ':00:00',
            'PRS': info['PRS'],
            'PRS_Sea': info['PRS_Sea'],
            'PRS_Max': info['PRS_Max'],
            'PRS_Min': info['PRS_Min'],
            'TEM': info['TEM'],
            'TEM_MAX': info['TEM_MAX'],
            'TEM_MIN': info['TEM_MIN'],
            'RHU': info['RHU'],
            'RHU_Min': info['RHU_Min'],
            'VAP': info['VAP'],
            'PRE_3h': info['PRE_3h'],
            'WIN_S_MAX': info['WIN_S_MAX'],
            'WIN_S_Inst_Max': info['WIN_S_Inst_Max'],
            'CLO_Cov': info['CLO_Cov'],
            'CLO_Cov_Low': info['CLO_Cov_Low']
        }
        infos.append(element)

    filename = 'data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile,
                            fieldnames=['Station_Id_C', 'ds', 'PRS', 'PRS_Sea', 'PRS_Max', 'PRS_Min', 'PRS_Min', 'TEM',
                                        'TEM_MAX', 'TEM_MIN', 'RHU', 'RHU_Min', 'VAP', 'PRE_3h', 'WIN_S_MAX',
                                        'WIN_S_Inst_Max', 'CLO_Cov', 'CLO_Cov_Low'])
        writer.writeheader()
        writer.writerows(infos)
    df = pd.read_csv('data.csv')

    df_PRS = df[['Station_Id_C', 'ds', 'PRS']]
    df_PRS_Sea = df[['Station_Id_C', 'ds', 'PRS_Sea']]
    df_PRS_Max = df[['Station_Id_C', 'ds', 'PRS_Max']]
    df_PRS_Min = df[['Station_Id_C', 'ds', 'PRS_Min']]
    df_TEM = df[['Station_Id_C', 'ds', 'TEM']]
    df_TEM_MAX = df[['Station_Id_C', 'ds', 'TEM_MAX']]
    df_TEM_MIN = df[['Station_Id_C', 'ds', 'TEM_MIN']]
    df_RHU = df[['Station_Id_C', 'ds', 'RHU']]
    df_RHU_Min = df[['Station_Id_C', 'ds', 'RHU_Min']]
    df_VAP = df[['Station_Id_C', 'ds', 'VAP']]
    df_PRE_3h = df[['Station_Id_C', 'ds', 'PRE_3h']]
    df_WIN_S_MAX = df[['Station_Id_C', 'ds', 'WIN_S_MAX']]
    df_WIN_S_Inst_Max = df[['Station_Id_C', 'ds', 'WIN_S_Inst_Max']]
    df_CLO_Cov = df[['Station_Id_C', 'ds', 'CLO_Cov']]
    df_CLO_Cov_Low = df[['Station_Id_C', 'ds', 'CLO_Cov_Low']]

    station_id = request.GET.get("station_id")
    timegpt_fcst_PRS = nixtla_client.forecast(df=df_PRS, h=24, freq='h', target_col='PRS')
    timegpt_fcst_PRS_Sea = nixtla_client.forecast(df=df_PRS_Sea, h=24, freq='h', target_col='PRS_Sea')
    timegpt_fcst_PRS_Max = nixtla_client.forecast(df=df_PRS_Max, h=24, freq='h', target_col='PRS_Max')
    timegpt_fcst_PRS_Min = nixtla_client.forecast(df=df_PRS_Min, h=24, freq='h', target_col='PRS_Min')
    timegpt_fcst_TEM = nixtla_client.forecast(df=df_TEM, h=24, freq='h', target_col='TEM')
    timegpt_fcst_TEM_MAX = nixtla_client.forecast(df=df_TEM_MAX, h=24, freq='h', target_col='TEM_MAX')
    timegpt_fcst_TEM_MIN = nixtla_client.forecast(df=df_TEM_MIN, h=24, freq='h', target_col='TEM_MIN')
    timegpt_fcst_RHU = nixtla_client.forecast(df=df_RHU, h=24, freq='h', target_col='RHU')
    timegpt_fcst_RHU_Min = nixtla_client.forecast(df=df_RHU_Min, h=24, freq='h', target_col='RHU_Min')
    timegpt_fcst_VAP = nixtla_client.forecast(df=df_VAP, h=24, freq='h', target_col='VAP')
    timegpt_fcst_PRE_3h = nixtla_client.forecast(df=df_PRE_3h, h=24, freq='h', target_col='PRE_3h')
    timegpt_fcst_WIN_S_MAX = nixtla_client.forecast(df=df_WIN_S_MAX, h=24, freq='h', target_col='WIN_S_MAX')
    timegpt_fcst_WIN_S_Inst_Max = nixtla_client.forecast(df=df_WIN_S_Inst_Max, h=24, freq='h',
                                                         target_col='WIN_S_Inst_Max')
    timegpt_fcst_CLO_Cov = nixtla_client.forecast(df=df_CLO_Cov, h=24, freq='h', target_col='CLO_Cov')
    # timegpt_fcst_CLO_Cov_Low = nixtla_client.forecast(df=df_CLO_Cov_Low, h=24, freq='h', target_col='CLO_Cov_Low')
    merge = pd.DataFrame({
        'Station_Id_C': [station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id, station_id, station_id, station_id, station_id, station_id,
                         station_id, station_id, station_id],
        'ds': timegpt_fcst_PRS['ds'],
        'PRS': timegpt_fcst_PRS['TimeGPT'],
        'PRS_Sea': timegpt_fcst_PRS_Sea['TimeGPT'],
        'PRS_Max': timegpt_fcst_PRS_Max['TimeGPT'],
        'PRS_Min': timegpt_fcst_PRS_Min['TimeGPT'],
        'TEM': timegpt_fcst_TEM['TimeGPT'],
        'TEM_MAX': timegpt_fcst_TEM_MAX['TimeGPT'],
        'TEM_MIN': timegpt_fcst_TEM_MIN['TimeGPT'],
        'RHU': timegpt_fcst_RHU['TimeGPT'],
        'RHU_Min': timegpt_fcst_RHU_Min['TimeGPT'],
        'VAP': timegpt_fcst_VAP['TimeGPT'],
        'PRE_3h': timegpt_fcst_PRE_3h['TimeGPT'],
        'WIN_S_MAX': timegpt_fcst_WIN_S_MAX['TimeGPT'],
        'WIN_S_Inst_Max': timegpt_fcst_WIN_S_Inst_Max['TimeGPT'],
        'CLO_Cov': timegpt_fcst_CLO_Cov['TimeGPT'],
        # 'CLO_Cov_Low': timegpt_fcst_CLO_Cov_Low['TimeGPT']
    })
    merge.to_csv('output.csv', index=False)
    future_ex_vars_df = pd.read_csv('output.csv')
    forecast_df = nixtla_client.forecast(
        df=df,
        X_df=future_ex_vars_df,
        h=24,
        freq='h',
        id_col='Station_Id_C',
        target_col='PRS',
        time_col='ds'
    )
    data = forecast_df.to_dict()
    resp_body = {"status_code": StatusCode.OK.value, "message": "SUCCESS", "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
