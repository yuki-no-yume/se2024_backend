from django.db import models
from datetime import datetime,timezone
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    type = (
        ('1', '普通用户'),
        ('2', '灾害发布管理员'),
        ('3',"灾害审核管理员")
    )
    email = models.EmailField(unique=True) # django验证,有效期
    username = models.CharField(max_length=32, verbose_name="用户名") #默认邮箱
    password = models.CharField(max_length=64,default='111111')
    level = models.CharField(max_length=3,choices=type,default='1')
    confirmed = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime(1970,1,1,tzinfo=timezone.utc)) # 验证码发送时间
    ver_code = models.CharField(max_length=6)

    def save(self,*args,**kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args,**kwargs)

    def to_dict(self):
        return {
            "user_id":self.id,
            "username":self.username,
            "email":str(self.email),
            "level":dict(self.type).get(self.level, '未知用户类型'),
        }


class Subscribed(models.Model):  # 订阅城市
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name='notAdmin')
    city = models.CharField(max_length=20)

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "city": self.city,
        }
