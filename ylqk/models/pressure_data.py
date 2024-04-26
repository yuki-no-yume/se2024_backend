from django.db import models


class PressureData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.IntegerField()
    PRS = models.FloatField()
    PRS_Sea = models.FloatField()
    PRS_Max = models.FloatField()
    PRS_Min = models.FloatField()
    station_info = None

    class Meta:
        db_table = "current_meteorological_data"

    def to_dict(self):
        return {
            "station_info": self.station_info.to_dict(),
            "datetime": str(self.Datetime),
            "pressure": self.PRS,
            "pressure_sea": self.PRS_Sea,
            "pressure_max": self.PRS_Max,
            "pressure_min": self.PRS_Min,
        }
