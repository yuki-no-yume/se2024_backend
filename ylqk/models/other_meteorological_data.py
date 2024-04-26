from django.db import models

from ylqk.models.station_info import StationInfo


class OtherMeteorologicalData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    WEP_Now = models.FloatField()
    VIS = models.FloatField()
    station_info: StationInfo = None

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
