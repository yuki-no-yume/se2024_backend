from django.db import models

from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    type = (
        ('1', '普通用户'),
        ('2', '信息管理员'),
    )
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=64)
    token = models.CharField(max_length=64,null=True,blank=True)
    email = models.EmailField()
    level = models.CharField(max_length=3,choices=type)


class Subscribed(models.Model):  # 订阅城市
    user = models.ForeignKey(to='UserProfile', to_field='id', on_delete=models.CASCADE, related_name='notAdmin')
    city = models.CharField(max_length=20)
