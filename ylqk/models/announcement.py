from django.db import models
from polymorphic.models import PolymorphicModel

# 模型输出还没确定
class AIDisasterForecast(models.Model):
    datatime = models.DateTimeField(auto_now_add=True)
    disaster_type = models.CharField(max_length=10)
    disaster_level = models.IntegerField()
    disaster_location = models.CharField(max_length=20)
    disaster_longitude = models.FloatField()
    disaster_latitude = models.FloatField()

    def to_dict(self):
        return {
            "datatime": str(self.datatime),
            "disaster_type": self.disaster_type,
            "disaster_level": self.disaster_level,
            "disaster_location": self.disaster_location,
            "disaster_longitude": self.disaster_longitude,
            "disaster_latitude": self.disaster_latitude,
        }


class Announcement(PolymorphicModel):
    time = models.DateTimeField(auto_now_add=True)



class ForewarnForUser(Announcement):
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE,related_name="user_relate")

    class Meta:
        db_table = "user_announcements"

    def to_dict(self):
        return {
            "time":str(self.time),
            "disaster":self.disaster.to_dict(),
            "user":self.user.to_dict(),
        }


class ForecastForAdmin(Announcement):
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    class Meta:
        db_table = "admin_announcements"

    def to_dict(self):
        return {
            "time":str(self.time),
            "disaster":self.disaster.to_dict(),
            "confirmed":self.confirmed,
        }


class ApplicationForGlobal(Announcement):
    content = models.CharField(max_length=300,default="")

    class Meta:
        db_table = "global_announcement"

    def to_dict(self):
        return {
            "time":str(self.time),
            "content":self.content,
        }

#
# class NormalMessage(Announcement):
#     sender = models.ForeignKey(to='UserProfile',to_field='id',on_delete=models.CASCADE,related_name='beginwithuser') # 发件人
#     receiver = models.ForeignKey(to='UserProfile',to_field='id',on_delete=models.CASCADE,related_name='beginwithadmin') # 收件人
#     message_object = models.ForeignKey(to='UserProfile',to_field='id',on_delete=models.CASCADE,related_name='user') # 处理对象
#
#     class Meta:
#         db_table = "personal_announcement"