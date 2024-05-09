from django.db import models

from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    type = (
        ('1', '普通用户'),
        ('2', '信息管理员'),
    )
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64)
    email = models.EmailField()
    level = models.CharField(max_length=3,choices=type)

    def to_dict(self):
        return {
            "user_id":self.id,
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "level":self.level,
        }


class Subscribed(models.Model):  # 订阅城市
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name='notAdmin')
    city = models.CharField(max_length=20)

    def to_dict(self):
        return {
            "user": self.user.to_dict(),
            "city": self.city,
        }
