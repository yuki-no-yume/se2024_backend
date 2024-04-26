from django.db import models


class StationInfo(models.Model):
    station_id = models.IntegerField(primary_key=True)
    province = models.CharField(max_length=32)
    station_name = models.CharField(max_length=32)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        db_table = "station_info"

    def to_dict(self) -> dict:
        return {
            "station_id": self.station_id,
            "province": self.province,
            "station_name": self.station_name,
            "longitude": self.longitude,
            "latitude": self.latitude
        }
