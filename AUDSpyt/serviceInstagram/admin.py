from django.contrib import admin

from .models import instagramActivity, instagramUser, instagramDirect, comentarios
# Register your models here.

admin.site.register(instagramActivity)
admin.site.register(instagramUser)
admin.site.register(instagramDirect)
admin.site.register(comentarios)
