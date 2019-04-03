import json
from django.shortcuts import render
from InstagramAPI import InstagramAPI
from django.http import HttpResponse




def ff(self):
    instagramAPI.getSelfGeoMedia(self)


def loginresult(request, foo):
    if (foo):
        instagramAPI.getSelfUserFeed()  # get self user feed
        return HttpResponse('<h2> Detail user Id :' + instagramAPI.LastJson + ' </h2>')
    else:
        return HttpResponse('<h2> Detail user Id :' + "Can't login!" + ' </h2>')

instagramAPI = InstagramAPI("taeusdsspyt", "test.pyt")
foo = instagramAPI.login()

loginresult(instagramAPI, foo)
# login
#mediaId = '1469246128528859784_1520706701'    # a media_id
#recipients = []                             # array of user_ids. They can be strings or ints
#InstagramAPI.direct_share(mediaId, recipients, text='aquest es es darrer')
# Create your views here.
