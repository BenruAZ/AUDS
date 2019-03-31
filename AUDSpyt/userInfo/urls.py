from django.urls import path
from . import views

urlpatterns = [
    # /userInfo/
    path('', views.index, name='index'),
    # /userInfo/id
    path('<int:user_id>/', views.detail, name='detail'),
]