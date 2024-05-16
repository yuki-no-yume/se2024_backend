from django.contrib import admin

from .models.users import *
from .models.announcement import *

# Register your models here.
# 超级管理员功能
admin.site.register(UserProfile)
admin.site.register(ApplicationForGlobal)

# 仅用于测试
admin.site.register(Subscribed)
admin.site.register(Announcement)
admin.site.register(AIDisasterForecast)
admin.site.register(ForecastForAdmin)
admin.site.register(ForewarnForUser)

