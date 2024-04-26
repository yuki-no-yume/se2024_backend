from django.db import models

from ylqk.models.station_info import StationInfo


class WindData(models.Model):
    Station_Id_C = models.IntegerField(primary_key=True)
    Datetime = models.DateTimeField()
    WIN_S_Avg_2mi = models.FloatField()
    WIN_D_Avg_2mi = models.IntegerField()
    WIN_S_MAX = models.FloatField()
    WIN_D_S_Max = models.IntegerField()
    WIN_S_Inst_Max = models.FloatField()
    WIN_D_INST_Max = models.IntegerField()
    station_info: StationInfo = None

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