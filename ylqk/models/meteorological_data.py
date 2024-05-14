from django.db import models

from ylqk.models.station_info import StationInfo


class AllMeteorologicalData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    PRS = models.FloatField()
    PRS_Sea = models.FloatField()
    PRS_Max = models.FloatField()
    PRS_Min = models.FloatField()
    TEM = models.FloatField()
    TEM_MAX = models.FloatField()
    TEM_MIN = models.FloatField()
    RHU = models.IntegerField()
    RHU_Min = models.IntegerField()
    VAP = models.FloatField()
    PRE_3h = models.FloatField()
    WIN_S_Avg_2mi = models.FloatField()
    WIN_D_Avg_2mi = models.IntegerField()
    WIN_S_MAX = models.FloatField()
    WIN_D_S_Max = models.IntegerField()
    WIN_S_Inst_Max = models.FloatField()
    WIN_D_INST_Max = models.IntegerField()
    CLO_Cov = models.IntegerField()
    CLO_Cov_Low = models.IntegerField()
    CLO_COV_LM = models.IntegerField()
    WEP_Now = models.FloatField()
    VIS = models.FloatField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),

            "temperature": self.TEM,
            "temperature_max": self.TEM_MAX,
            "temperature_min": self.TEM_MIN,

            "pressure": self.PRS,
            "pressure_sea": self.PRS_Sea,
            "pressure_max": self.PRS_Max,
            "pressure_min": self.PRS_Min,

            "relative_humidity": self.RHU,
            "relative_humidity_min": self.RHU_Min,
            "vapor_pressure": self.VAP,
            "precipitation_in_3h": self.PRE_3h,

            "wind_speed_average_in_2min": self.WIN_S_Avg_2mi,
            "wind_direction_average_in_2min": self.WIN_D_Avg_2mi,
            "wind_speed_max": self.WIN_S_MAX,
            "wind_direction_of_speed_max": self.WIN_D_S_Max,
            "wind_speed_of_instant_max": self.WIN_S_Inst_Max,
            "wind_direction_of_instant_max": self.WIN_D_INST_Max,

            "cloud_cover_total": self.CLO_Cov,
            "cloud_cover_low": self.CLO_Cov_Low,
            "cloud_cover_low_and_mid": self.CLO_COV_LM,

            "current_weather": self.WEP_Now,
            "visibility": self.VIS,
        }


class PressureData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    PRS = models.FloatField()
    PRS_Sea = models.FloatField()
    PRS_Max = models.FloatField()
    PRS_Min = models.FloatField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "pressure": self.PRS,
            "pressure_sea": self.PRS_Sea,
            "pressure_max": self.PRS_Max,
            "pressure_min": self.PRS_Min,
        }


class TemperatureData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    TEM = models.FloatField()
    TEM_MAX = models.FloatField()
    TEM_MIN = models.FloatField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "temperature": self.TEM,
            "temperature_max": self.TEM_MAX,
            "temperature_min": self.TEM_MIN,
        }


class HumidityData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    RHU = models.IntegerField()
    RHU_Min = models.IntegerField()
    VAP = models.FloatField()
    PRE_3h = models.FloatField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "relative_humidity": self.RHU,
            "relative_humidity_min": self.RHU_Min,
            "vapor_pressure": self.VAP,
            "precipitation_in_3h": self.PRE_3h,
        }


class WindData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    WIN_S_Avg_2mi = models.FloatField()
    WIN_D_Avg_2mi = models.IntegerField()
    WIN_S_MAX = models.FloatField()
    WIN_D_S_Max = models.IntegerField()
    WIN_S_Inst_Max = models.FloatField()
    WIN_D_INST_Max = models.IntegerField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "wind_speed_average_in_2min": self.WIN_S_Avg_2mi,
            "wind_direction_average_in_2min": self.WIN_D_Avg_2mi,
            "wind_speed_max": self.WIN_S_MAX,
            "wind_direction_of_speed_max": self.WIN_D_S_Max,
            "wind_speed_of_instant_max": self.WIN_S_Inst_Max,
            "wind_direction_of_instant_max": self.WIN_D_INST_Max,
        }


class CloudData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    CLO_Cov = models.IntegerField()
    CLO_Cov_Low = models.IntegerField()
    CLO_COV_LM = models.IntegerField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "cloud_cover_total": self.CLO_Cov,
            "cloud_cover_low": self.CLO_Cov_Low,
            "cloud_cover_low_and_mid": self.CLO_COV_LM,
        }


class OtherMeteorologicalData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    WEP_Now = models.FloatField()
    VIS = models.FloatField()
    station_info: StationInfo

    class Meta:
        db_table = "current_meteorological_data"
        managed = False

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "current_weather": self.WEP_Now,
            "visibility": self.VIS,
        }
