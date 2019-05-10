from django.urls import path
from . import views

urlpatterns = [
    # /insta/
    path('', views.intagrampruebas, name='intagrampruebas'),
    path('1', views.intagrampruebas1, name='intagrampruebas1'),
    # /userInfo/id
    # path('<int:user_id>/', views.detail, name='detail'),
]