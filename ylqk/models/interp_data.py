from django.db import models


class InterpData(models.Model):
    longitude = models.FloatField(primary_key=True)
    latitude = models.FloatField()
    temp = models.FloatField()
    prs = models.FloatField()
    rhu = models.FloatField()
    pre3h = models.FloatField()
    wind_s = models.FloatField()

    class Meta:
        db_table = "interp_meteorological_data"
        managed = False
