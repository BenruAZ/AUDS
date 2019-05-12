from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # /insta/
    path('43', views.intagrampruebas, name='intagrampruebas'),
    path('1', views.intagrampruebas1, name='intagrampruebas1'),
    path('prMain', views.prMain, name='prMain'),
    # /insta/id
    path('prDetAct/<int:actvId>/', views.prMainActDet, name='actDetail'),
    path('prDetUs/<int:usId>/', views.prMainUsDet, name='prMainUserDetail'),
    path('prUpdateComment/<int:actvId>/', views.updateActivityComments, name='updateActivityComments'),
  ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)