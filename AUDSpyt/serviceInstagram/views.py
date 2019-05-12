import logging
import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from AUDSpyt.settings import BASE_DIR
from .models import instagramActivity, instagramDirect,instagramUser,comentarios
from actividades.models import Activity
from userInfo.models import UserInfo
import json
from InstagramAPI import InstagramAPI

# Create your views here.

def updateActivityComments(request,actvId):
    from .models import instagramActivity
    from actividades.models import Activity

    retunrstring = ''
    ee = instagramActivity.objects.filter(actividad_id = actvId).first()
    if ee != None:
        pp = ee.serchComentarios()

        return HttpResponse(retunrstring + ' ----------------- ' + str(pp))

def prMainUsDet(request, usId):
    ui = get_object_or_404(UserInfo, pk=usId)
    iu = instagramUser.objects.filter(userInfo = ui).first()
    com = comentarios.objects.filter(instaUser__in =(instagramUser.objects.filter(userInfo = ui)))
    logging.warning('Usuario Detalle '+str(ui.pk))
    logging.warning('com ' + str(com))
    context = {
        'iu':iu,
        'ui': ui,
        'com': com
    }
    return render(request, os.path.join(os.path.join(BASE_DIR, 'templates', 'userDetail.html')), context)
def prMainActDet(request, actvId):
    actv = get_object_or_404(Activity, pk=actvId)
    logging.warning('Actividad Detalle '+str(actv.pk))
    insActv = instagramActivity.objects.filter(actividad = actv).first()
    photo = '/IconoActividad/thirdAUDS.jpg'
    logging.warning('isact '+str(insActv) )
    com = comentarios.objects.filter(activity__in = (instagramActivity.objects.filter(actividad = actv)))
    logging.warning('com ' + str(com))

    for c in com:
        logging.warning('photo ' + str(actv.icono))

    context = {
        'photo':'/' + str(actv.icono),
        'actv': actv,
        'insActv': insActv,
        'com': com
    }
    return render(request, os.path.join(os.path.join(BASE_DIR, 'templates', 'actividadDetalle.html')), context)
def prMain(request):
    all_insAct = instagramActivity.objects.all().order_by('-actividad')
    icomentarios = comentarios.objects.all()
    users = UserInfo.objects.all()

    #html_actividades = Activity.objects.all()
    #html_estadisticas = ''
    context = {
        'all_insAct': all_insAct,
        'icomentarios': icomentarios,
        'users': users
        #'html_estadisticas': html_estadisticas,

    }
    logging.warning('allactivities ' + str(all_insAct))
    return render(request, os.path.join(os.path.join(BASE_DIR,'templates','activityDetShort.html')), context)

def index(request):
    all_users = UserInfo.objects.all()
    context = {
        'all_users': all_users,
    }
    return render(request, 'userIndex.html', context)

def intagrampruebas1(request):
    from .models import instagramActivity
    from actividades.models import Activity

    retunrstring = ''
    ee = instagramActivity.objects.all()[1]
    if ee != None:
        pp = ee.serchComentarios()

        return HttpResponse(retunrstring + ' ----------------- ' + str(pp))

def intagrampruebas(request):
    retunrstring = ''
    api = InstagramAPI("taeusdsspyt", "test.pyt")
    api.login()

    retunrstring += str(api.LastJson)
    all_users = UserInfo.objects.all()
    all_activities = Activity.objects.all()
    #objects.get(name="")

    user = all_users[0]
    act = all_activities[0]

    insact = instagramActivity()
    insact.setInsAct(act)

    insact.subirActividad(api)
    retunrstring = str(api.LastJson)
    str(act.icono)
    return HttpResponse(retunrstring + ' ----------------- ' + str(act.icono))