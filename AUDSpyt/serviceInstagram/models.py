#from os import path
import time

from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

from AUDSpyt.settings import BASE_DIR
from actividades.models import Activity
from userInfo.models import UserInfo
from django.db import models
import logging
from datetime import datetime

import json
from InstagramAPI import InstagramAPI, os


class instagramActivity(models.Model):
    actividad = models.ForeignKey(Activity, on_delete=models.CASCADE)
    instaId = models.CharField(primary_key=True, max_length=250)
    likes = models.IntegerField(default=-1)
    uploaded = models.BooleanField(default=False)
    url = models.CharField(max_length=250, default='anonimous')
    #Anadir Code para URL


    def setInsAct(self, act2set):
       # time.sleep(2)
        self.actividad = act2set
        api = InstagramAPI("taeusdsspyt", "test.pyt")
        api.login()
        logging.warning('Login json: ' + str(api.LastJson))
        tmpbool = self.subirActividad(api)
        logging.warning('subir Actividad resultado: ' + str(tmpbool))
        ev = api.LastJson
        logging.warning('Upload image result json: ' + str(ev))
        logging.warning('Upload image STATUS-result json: ' + str(ev.get("status")))
        if ev.get("status") == "ok":
            self.uploaded = True
            self.getIdfromLastIA(api)



    def __str__(self):
        return self.actividad.titulo
#FORMATEAR LA FECHA
    def subirActividad(self, api):
        #acc = Activity.objects.get(pk=self.pk)
        #image =  Image.open(self.actividad.icono)
        #image.save(self.actividad.icono)
        tmpImg = self.actividad.icono.open()
        logging.warning('act ' + self.actividad.icono.url)
        act = Activity.objects.filter(pk = self.actividad.pk).first()
        logging.warning('PPOOODODOOODDODOODODOD ' + act.icono.url)
        tmpImg = self.actividad.icono.open()
        # tmpImg.save()
        #tmpImg.save(tmpImg)
        #photo=str(tmpImg)
        api.uploadPhoto(str(tmpImg.path), caption=str(self.actividad.fechaFinal) + ' ' +
                                                           self.actividad.titulo + ' ' +
                                                           self.actividad.descripcionCorta
                        )

        uploadResume = api.LastJson
        if uploadResume.get('status') != 'fail':
            self.getIdfromLastIA(api)
        else:
            logging.warning('------FOTO UPLOADED RESUME ------' + str(uploadResume))
#MEJORAR INCLUYENDO IDENTIFICADORES UNICOS A LAS FOTOS
    def getIdfromLastIA(self, api):
        api.getSelfUserFeed()
        userFeedJson = api.LastJson
        postJson = userFeedJson.get('items')
        #LOG
        logging.warning('Self User Feed Activities: ' + str(postJson))
        logging.warning('Last Post Id: ' + str(postJson[0].get('id')))
        logging.warning('Last Post C0de: ' + str(postJson[0].get('code')))
        #LOG
        self.instaId = str(postJson[0].get('id'))
        self.url = str(postJson[0].get('code'))

    def serchComentarios(self):
        anonimUser = instagramUser.objects.get(pk=1)
        api = InstagramAPI("taeusdsspyt", "test.pyt")
        api.login()
        has_more_comments = True
        max_id = ''
        anonimComments = []

        logging.warning('Media Id ' + self.instaId)

        while has_more_comments:
            api.getMediaComments(self.instaId, max_id=max_id)
            commentsJson = api.LastJson
            logging.warning('comentJsonBug: ' + str(commentsJson.get('comments')))

            #verificar usuarios
            tmpUsList = []
            for tmpComment in commentsJson.get('comments'):
                tmpUsList.append(str(tmpComment.get('user_id')))
            if len(tmpUsList)!= 0:
                userList = instagramUser.objects.filter(pk__in=tmpUsList)
                logging.warning('logged comment user ' + str(userList))
            else:
                logging.warning('Not logged user comments')

            #Despues de sacar la lista de intagram user la asignamos en este bucle
            for tmpComment in commentsJson.get('comments'):
                if len(userList) != 0:
                    self.setComentUser(userList, tmpComment, anonimComments)
                else:
                    anonimComments.append(tmpComment)
            self.setComentUserAnonim(anonimComments , anonimUser)
                    #logging.warning('No registered Users on new comments')
            has_more_comments = commentsJson.get('has_more_comments', False)
            if has_more_comments:
                max_id = commentsJson.get('next_max_id', '')
                time.sleep(2)
                #logging.warning('Comment Json: ' + str(commensJson))


        return 'Comment Json: ' + str(commentsJson.get('comments'))

        #else:
            #logging.warning('Instagram activity not set')
            #return 'Instagram activity not set'

    def setComentUser(self, userList, tmpComment, anonimComments):
        bll = True
        for tmpUser in userList:
            comentario = comentarios()
            if tmpUser.instaId == str(tmpComment.get('user_id')):
                self.setComentUserAux(tmpUser, tmpComment)
                bll = False
        if bll:
            anonimComments.append(tmpComment)

    def setComentUserAnonim(self, anonimComments , anonimUser):
        for tmpComment in anonimComments:
            logging.warning('Anonimous Comment Added')
            self.setComentUserAux(anonimUser,tmpComment)


    def setComentUserAux(self, tmpUser, tmpComment):
            comentario = comentarios()

            logging.warning(
                'Comment : ' + str(tmpComment.get('pk')) + ' ' + str(tmpComment.get('text')) + ' ' + str(
                    tmpComment.get('user_id')) + ' ' + str(tmpComment.get('created_at')))
            comentario.setComentario(
                # instaUser=instagramUser.objects.create(instaId=str(tmpComment.get('user_id')), userInfo=anonimUser),
                instaId=str(tmpComment.get('pk')),
                instaUser=tmpUser,
                activity=self,
                likes=int(tmpComment.get('comment_like_count')),
                texto=str(tmpComment.get('text')),
                fecha=datetime.fromtimestamp(int(tmpComment.get('created_at')))
            )
            if tmpUser.instaId == '1':
                comentario.instaUserAnonim = str(tmpComment.get('user_id'))
            comentario.save()

    def verificarUsuario(self, listaComentarios):
        listaUsuarios = []
        for tmpComentario in listaComentarios:

            p = instagramUser.objects.filter(instaId=comentarios(tmpComentario).instaUser.instaId).first()
            if p != None:
                listaUsuarios.append(p)
        comentariosVerificados = self.compararUsuarios(listaUsuarios, listaComentarios)
        for savecomm in comentariosVerificados:
            comentarios(savecomm).save()



    def compararUsuarios(self, listaComentariosSV , listaUsuarios):
        comentariosGuardar = []
        for tmpUser in listaUsuarios:
            for tmpComment in listaComentariosSV:
                if tmpComment.instaId == tmpUser.instaId:
                    comentariosGuardar.append(tmpComment)
                    tmpComment.save()
        return comentariosGuardar






    @receiver(post_save, sender= Activity)
    def addActivity(sender, instance, **kwargs):
        #instance is the object that triggers
        if instance.publicarInstagram:
            instAct = instagramActivity()
            instAct.setInsAct(instance)
            instAct.save()

    def hola(self):
        return


class instagramUser(models.Model):
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    instaId = models.CharField(primary_key=True, max_length=250)
    #Add instaId como Id de Django para

    def setInstagramUser(self, userInfo):
        api = InstagramAPI("taeusdsspyt", "test.pyt")
        api.login()
        self.userInfo = userInfo
        self.idFromUsername(api)
       # logging.warning('User Json: ' + str(api.LastJson))


    def __str__(self):
        return self.userInfo.contacto

    def idFromUsername(self, api):
        #La URL se obtiene directamente con el UserName
        #Nuestro valor buscado es el instagramId y si lo ha encontrado

        api.searchUsername(self.userInfo.contacto)
        tmpJson = api.LastJson
        logging.warning(str(tmpJson))
        if api.LastJson.get('status') == 'ok':
            iUserPK = str(tmpJson.get('user').get('pk'))
            self.pk = iUserPK
            self.save()
            logging.warning('User PK: ' + iUserPK)
        elif api.LastJson.get('status') == 'fail':
            logging.warning('Failure msg: ' + str(tmpJson.get('message')))




class instagramDirect(models.Model):
    instaUser = models.ForeignKey(instagramUser, on_delete=models.CASCADE)
    instaId = models.CharField(max_length=250)
    mensage = models.CharField(max_length=250)
    reverse = models.BooleanField(default=False)

    def getAllmsg(self, api):
        #api = InstagramAPI("login", "password")
        #api.login()
        return api.getDirectShare()

    def sendmsg(self, api):
        api.direct_share(self.instaId, text=self.mensage)

class comentarios(models.Model):
    instaId = models.CharField(primary_key=True, max_length=250)
    instaUser = models.ForeignKey(instagramUser, on_delete=models.CASCADE)
    instaUserAnonim = models.CharField(max_length=250)
    activity = models.ForeignKey(instagramActivity, on_delete=models.CASCADE)
    likes = models.IntegerField()
    texto = models.CharField(max_length=250)
    fecha = models.DateTimeField(editable=False)
    #trigger on update para guardar versiones en cambios en los comentarios
    def __str__(self):
        return str(self.fecha) + ' ' + self.texto

    def setComentario(self,instaId, instaUser, activity, likes, texto, fecha):
        self.instaId = instaId
        self.activity = activity
        self.instaUser = instaUser
        self.likes = likes
        self.texto = texto
        self.fecha = fecha

    def comprobarDobleVotacion(self, actividad):
        instaUsers = instagramUser.objects.all()
        #nstagramUser.objects.filter(pk__in=
          #                       instagramUser.objects.order_by().values('author_id').annotate(
        #                        max_id=models.Max('id')).values('max_id'))

class instagramSession(models.Model):
    sesionjson = models.CharField(max_length=250)
    active = models.BooleanField(default=True)

    def setNotActive(self):
        self.active=False

    def login(self):
        api = InstagramAPI("taeusdsspyt", "test.pyt")
        if api.login() != False:
            logging.warning('Login Json: ' + str(api.LastJson))

