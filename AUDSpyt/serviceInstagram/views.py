from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import instagramActivity, instagramDirect,instagramUser,comentarios
from actividades.models import Activity
from userInfo.models import UserInfo
import json
from InstagramAPI import InstagramAPI

# Create your views here.

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