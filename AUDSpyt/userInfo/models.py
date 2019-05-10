from django.db import models
from django.utils import timezone

# Create your models here.
class UserInfo(models.Model):
    MODALIDAES_SKATE = (
        ('Skate', 'Skateboarding'),
        ('BMX', 'BMX'),
        ('Roller', 'Rollerbladin'),
    )
    ESTILO_PATINAJE =(
        ('Rampa','Rampa'),
        ('Calle', 'Calle'),
        ('Ambas', 'Ambas'),
    )
    nombre = models.CharField(max_length=250)
    apellido1 = models.CharField(max_length=250)
    apellido2 = models.CharField(max_length=250)
    DNI = models.CharField(max_length=250)
    fecha_nacimiento = models.DateField()
    correo = models.EmailField()
    modalidad = models.CharField(max_length=250, choices=MODALIDAES_SKATE)
    estilo = models.CharField(max_length=250, choices=ESTILO_PATINAJE)
    skatepark = models.CharField(max_length=250) #Futura localizacion
    residencia = models.CharField(max_length=250)
    fecha_creacion = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    contacto = models.CharField(max_length=250)


    def __str__(self):
        return self.nombre + ' ' + self.apellido1

    def save(self, *args, **kwargs):
        if not self.id:
            self.fecha_creacion = timezone.now()
        self.modified = timezone.now()
        self.setinstaUser()
        return super(UserInfo, self).save(*args, **kwargs)

    def setinstaUser(self):
        if self.contacto != '':
            checkIUser = UserInfo.objects.filter(contacto=self.contacto).first()
            if checkIUser != None:
                from serviceInstagram.models import instagramUser
                newUser = instagramUser()
                newUser.setInstagramUser(self)
           # else:
            #    self.add_error('contacto', "El usuario ya tiene una cuenta asociada al contacro")


class User(models.Model):
    userInfo = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    cosasSeguridad = models.CharField(max_length=250)

