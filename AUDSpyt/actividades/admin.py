from django.contrib import admin
from .models import UserActivity, Activity
# Register your models here.
admin.site.register(Activity)
admin.site.register(UserActivity)
