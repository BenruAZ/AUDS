from django.db import models


# Create your models here.
class UserInfo(models.Model):
    nombre = models.CharField(max_length=250)
    apellido1 = models.CharField(max_length=250)
    apellido2 = models.CharField(max_length=250)
    DNI = models.CharField(max_length=250)
    fecha_nacimiento = models.CharField(max_length=250)
    correo = models.CharField(max_length=250)
    modalidad = models.CharField(max_length=250)
    estilo = models.CharField(max_length=250)
    skatepark = models.CharField(max_length=250)
    fecha = models.CharField(max_length=250)
    residencia = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre + ' ' + self.apellido1


class User(models.Model):
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    cosasSeguridad = models.CharField(max_length=250)

class Activity(models.Model):
    titulo = models.CharField(max_length=250)
    descripcionCorta =  models.CharField(max_length=250)
    descripcionLarga =  models.CharField(max_length=250)
    icono =  models.ImageField(upload_to = 'IconoActividad/', default = 'pic_folder/None/no-img.jpg')
    fechaFinal = models.CharField(max_length=250)
    #def RESUMEN USER ACTIVITY



class UserActivity(models.Model):
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    estado =  models.CharField(max_length=250) #Votacion(A favor - En contrA

