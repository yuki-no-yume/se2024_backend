from django.db import models

from ylqk.models.station_info import StationInfo


class TemperatureData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    TEM = models.FloatField()
    TEM_MAX = models.FloatField()
    TEM_MIN = models.FloatField()
    station_info: StationInfo = None

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
