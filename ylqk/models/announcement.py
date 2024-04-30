from django.db import models


# 模型输出还没确定
class AIDisasterForecast(models.Model):
    datatime = models.DateTimeField()
    disaster_type = models.CharField(max_length=10)
    disaster_level = models.IntegerField()
    disaster_location = models.CharField(max_length=20)
    disaster_longitude = models.FloatField()
    disaster_latitude = models.FloatField()

    def to_dict(self):
        return {
            "datatime": self.datatime,
            "disaster_type": self.disaster_type,
            "disaster_level": self.disaster_level,
            "disaster_location": self.disaster_location,
            "disaster_longitude": self.disaster_longitude,
            "disaster_latitude": self.disaster_latitude,
        }


class Announcement(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ForewarnForUser(Announcement):
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE,related_name="user_relate")

    class Meta:
        db_table = "user_announcements"


class ForecastForAdmin(Announcement):
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "admin_announcements"


class ApplicationForGlobal(Announcement):
    content = models.CharField(max_length=300)

    class Meta:
        db_table = "global_announcement"
