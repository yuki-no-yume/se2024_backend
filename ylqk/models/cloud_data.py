from django.db import models

from ylqk.models.station_info import StationInfo


class CloudData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    CLO_Cov = models.IntegerField()
    CLO_Cov_Low = models.IntegerField()
    CLO_COV_LM = models.IntegerField()
    station_info: StationInfo = None

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
