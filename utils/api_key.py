USER_ID = "715838905461wHwNl"
PWD = "IymUbtH"
BASIC_API = f"http://api.data.cma.cn:8090/api?userId={USER_ID}&pwd={PWD}" \
            "&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H"
ALL_ELEMENTS = "&elements=STATION_Id_C,Datetime,PRS,PRS_Sea,PRS_Max,PRS_Min," \
               "TEM,TEM_MAX,TEM_MIN," \
               "RHU,RHU_Min,VAP,PRE_3h," \
               "WIN_S_Avg_2mi,WIN_D_Avg_2mi,WIN_S_MAX,WIN_D_S_Max,WIN_S_Inst_Max,WIN_D_INST_Max," \
               "CLO_Cov,CLO_Cov_Low,CLO_COV_LM," \
               "VIS,WEP_Now"
