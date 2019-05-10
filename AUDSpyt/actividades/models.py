from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
import logging






class Activity(models.Model):
    titulo = models.CharField(max_length=250)
    descripcionCorta = models.CharField(max_length=250)
    descripcionLarga = models.CharField(max_length=250)
    icono = models.ImageField(upload_to='IconoActividad/')  # , default = 'pic_folder/None/no-img.jpg')
    fechaFinal = models.DateTimeField()
    publicarInstagram = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __str__(self):
        return self.titulo

    def setInsActivitynSave(self):
        from serviceInstagram.models import instagramActivity
        if self.publicarInstagram:
            inst = instagramActivity()
            inst.setInsAct(self)
            inst.save()

    def creationModificationdate(self):
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.modified = timezone.now()

    def save(self, *args, **kwargs):
        self.creationModificationdate()
        return super(Activity, self).save(*args, **kwargs)


    # def RESUMEN USER ACTIVITY
    # def ActivitytoInstagramPost
    # def onCascadeDMUserActivity


class UserActivity(models.Model):
    userInfo = models.ForeignKey('userInfo.UserInfo', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    estado = models.CharField(max_length=250)  # Votacion(A favor - En contra

    def setUserActivity(self, userInfo, activity, estado):
        #.get para 1 objeto
        #.filter para lista
        tmpUA = UserActivity.objects.filter(userInfo__pk = userInfo.pk, activity__pk = activity.pk).first()
        #tmpUA = UserActivity.objects.filter(userInfo__pk = userInfo.pk, activity__pk = activity.pk)
        if tmpUA == None :
            self.userInfo = userInfo
            self.activity = activity
            self.estado = estado
            self.save()
            return True
        else:
            logging.warning('User Activity registered for User :' + userInfo.nombre)
            logging.warning('Activity registered  :' + activity.titulo)
            return False
