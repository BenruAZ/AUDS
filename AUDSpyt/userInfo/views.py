from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import UserInfo
# Create your views here.
def index(request):
    all_users = UserInfo.objects.all()
    context = {
        'all_users': all_users,
    }
    return render(request, 'userIndex.html', context)

def detail(request, user_id):
    return HttpResponse('<h2> Detail user Id :'+ str(user_id) +' </h2>');