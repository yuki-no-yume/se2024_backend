from django.db import models

from ylqk.models.station_info import StationInfo


class HumidityData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    RHU = models.IntegerField()
    RHU_Min = models.IntegerField()
    VAP = models.FloatField()
    PRE_3h = models.FloatField()
    station_info: StationInfo = None

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
