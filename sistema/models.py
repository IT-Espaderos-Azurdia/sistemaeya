from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
import os

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Cobro(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.PositiveIntegerField()
    correo = models.EmailField(max_length=254)
    usuario = models.CharField(max_length=100,null=True,blank=True,unique=True)
    password = models.CharField(max_length=8,null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.nombre)

class CobroEmpresa(models.Model):
    precio = models.PositiveIntegerField()
    empresa = models.ForeignKey(Empresa,null=False,blank=False,on_delete=models.CASCADE)
    cobro = models.ForeignKey(Cobro,null=False,blank=False,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('empresa','cobro',)

class OperacionMes(models.Model):
    empresa = models.ForeignKey(Empresa,null=False,blank=False,on_delete=models.CASCADE)
    mes = models.PositiveIntegerField(null=False,blank=False,validators=[MinValueValidator(1),MaxValueValidator(12)])
    anio = models.PositiveIntegerField(null=False,blank=False,validators=[MinValueValidator(2016),MaxValueValidator(2300)])
    
    class Meta:
        unique_together =('empresa','mes','anio',)

class Abono(models.Model):
    operacionmes = models.ForeignKey(OperacionMes,null=True,blank=True,on_delete=models.CASCADE)
    monto = models.PositiveIntegerField(null=False,blank=False)
    fecha = models.DateField(null=False,blank=False)
    banco = models.CharField(null=True,blank=True,max_length=100)
    tipo = models.CharField(null=False,blank=False,max_length=100)
    recibio = models.CharField(null=False,blank=False,max_length=100)
    codigo = models.CharField(null=False,blank=False,max_length=100)
    fechadeposito = models.DateField(null=True,blank=True)
    codigodeposito = models.CharField(null=True,blank=True,max_length=100)


class Expediente(models.Model):
    cliente = models.CharField(null=True,blank=True,max_length=100)
    operacionmes = models.ForeignKey(OperacionMes,null=True,blank=True,on_delete=models.CASCADE)
    cobro = models.ManyToManyField(Cobro,blank=True)
    fecha_ingreso_oficina = models.DateField(null=False,blank=False)
    fecha_ingreso_digecam = models.DateField(null=True,blank=True)
    fecha_cita = models.DateField(null=True,blank=True)
    fecha_pago = models.DateField(null=True,blank=True)
    fecha_entrega = models.DateField(null=True,blank=True)
    recibio = models.CharField(null=True,blank=True,max_length=100)
    entrego = models.CharField(null=True,blank=True,max_length=50)
    tenencias = models.PositiveIntegerField(null=True,blank=True)
    #autenticadpi = models.PositiveIntegerField(null=True,blank=True)
    #autenticafirma = models.PositiveIntegerField(null=True,blank=True)
    #constanciaingresos = models.PositiveIntegerField(null=True,blank=True)
    #formularios = models.PositiveIntegerField(null=True,blank=True)
    estatus = models.CharField(null=False,blank=False,max_length=10)
    descripcion_estatus = models.CharField(null=True,blank=True,max_length=200)
    docfile = models.FileField(upload_to='archivos/',null=True,blank=True)
    numeroexpe = models.PositiveIntegerField(null=True,blank=True) #Numero Expediente



@receiver(models.signals.post_delete, sender=Expediente)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    
    if instance.docfile:
        if os.path.isfile(instance.docfile.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Expediente)
def auto_delete_file_on_change(sender, instance, **kwargs):
    
    if not instance.pk:
        return False

    try:
        old_file = Expediente.objects.get(pk=instance.pk).docfile
    except Expediente.DoesNotExist:
        return False

    new_file = instance.docfile
    if not old_file == new_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)