from django.db import models
from polymorphic.models import PolymorphicModel


# 模型输出还没确定
class AIDisasterForecast(models.Model):
    datatime = models.DateTimeField(auto_now_add=True)
    disaster_type = models.CharField(max_length=10)
    disaster_level = models.CharField(max_length=5)
    disaster_location = models.CharField(max_length=20)
    disaster_longitude = models.FloatField()
    disaster_latitude = models.FloatField()
    disaster_description = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "AIDisasterForecast"

    def to_dict(self):
        return {
            "id": self.id,
            "datatime": str(self.datatime),
            "disaster_type": self.disaster_type,
            "disaster_level": self.disaster_level,
            "disaster_location": self.disaster_location,
            "disaster_longitude": self.disaster_longitude,
            "disaster_latitude": self.disaster_latitude,
            "disaster_description": self.disaster_description,
        }


class Announcement(PolymorphicModel):
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = "abstract_announcement"

    def to_dict(self):
        return {
            "id": self.id,
            "time": str(self.time),
            "read": self.read,  # 是否已读
        }


class ForewarnForUser(Announcement):  # 通知用户
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name="user_relate")

    class Meta:
        db_table = "user_announcements"

    def to_dict(self):
        base_dict = super().to_dict()
        cur_dict = {
            "disaster": self.disaster.to_dict(),
            "user": self.user.to_dict(),
        }
        result_dict = {**base_dict, **cur_dict}
        return result_dict


class ForecastForAdmin(Announcement):  # 管理员间通信
    type = (
        ('0', "未知状态"),
        ('1', '首次提交'),
        ('2', '打回'),
        ('3', "修改后提交"),
        ('4', "允许发布"),
        ('5', '不允许发布'),
    )
    disaster = models.ForeignKey(to='AIDisasterForecast', to_field='id', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=type, default="0")
    send = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name='sender',
                             null=True, blank=True)  # 发件人
    rec = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name='receiver',
                            null=True, blank=True)  # 收件人
    remark = models.CharField(max_length=100, verbose_name='备注',null=True,blank=True)

    class Meta:
        db_table = "admin_announcements"

    def to_dict(self):
        base_dict = super().to_dict()
        cur_dict = {
            "disaster": self.disaster.to_dict(),
            "status": dict(self.type).get(self.status, '未知状态'),
            "sender": self.send.to_dict(),
            "receiver": self.rec.to_dict(),
            "remark": self.remark,
        }
        result_dict = {**base_dict, **cur_dict}
        return result_dict


class ApplicationForGlobal(Announcement):  # 系统通知，每个用户一个，不然影响已读，用的时候再说吧
    content = models.CharField(max_length=300, default="")

    class Meta:
        db_table = "global_announcements"

    def to_dict(self):
        base_dict = super().to_dict()
        cur_dict = {
            "content": self.content,
        }
        result_dict = {**base_dict, **cur_dict}
        return result_dict
