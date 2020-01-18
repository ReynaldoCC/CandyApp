from django.db import models
from django.contrib.auth.models import ContentType
from django.utils import timezone


# Put your mixins begin here
class ManagerMain(models.Manager):
    def get_queryset(self):
        return super(models.Manager, self).get_queryset().filter(deleted_at__isnull=True)


class ManagerAllMain(models.Manager):
    def get_queryset(self):
        return super(models.Manager, self).get_queryset()


## ACTIONFLAGS
# 0 -> Crear
# 1 -> Modificar
# 2 -> ELiminar
# 3 -> Login
# 4 -> Logout

class Log(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    action_flat = models.PositiveSmallIntegerField(null=True, blank=True)
    type_obj_id = models.IntegerField()
    type_obj_name = models.CharField(max_length=100)
    obj_id = models.IntegerField()
    obj_name = models.CharField(max_length=100)
    action_date = models.DateTimeField(auto_now_add=True)
    address = models.GenericIPAddressField(default='0.0.0.0')
    medical = models.BooleanField(default=False)

    class Meta:
        ordering = ('action_date', 'action_flat', )
        verbose_name_plural = 'Registros'
        verbose_name = 'Registro'


class LoggerMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    deleted_at = models.DateTimeField(auto_now=False, blank=True, auto_now_add=False, verbose_name='Eliminado', default=None, null=True)
    objects = ManagerMain()
    objects_all = ManagerAllMain()

    class Meta:
        abstract = True

    def perform_log(self, request=None, af=None):
        log = Log()
        if request.user and request.user.id:
            log.user_id = request.user.id
            log.user_name = request.user.username
        else:
            log.user_id = 0
            log.user_name = 'AnonymousUser'
        model_name = self.__class__.__name__.lower()
        obj_type = ContentType.objects.filter(model=model_name).first()
        log.action_flat = af or 4
        log.type_obj_id = obj_type.id
        log.type_obj_name = obj_type.name
        log.address = request.META['REMOTE_ADDR']
        log.obj_id = self.id
        log.obj_name = self.__str__()
        log.save()

    def save_and_log(self, request=None, af=None):
        self.save()
        self.perform_log(request=request, af=af)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def delete_flush(self, using=None, keep_parents=False):
        return super(models.Model, self).delete()


def perform_log(obj=None, request=None, af=None):
    log = Log()
    if request.user and request.user.id:
        log.user_id = request.user.id
        log.user_name = request.user.username
    else:
        log.user_id = 0
        log.user_name = 'AnonymousUser'
    model_name = obj.__class__.__name__.lower()
    obj_type = ContentType.objects.filter(model=model_name).first()
    log.action_flat = af or 4
    log.type_obj_id = obj_type.id
    log.type_obj_name = obj_type.name
    log.address = request.META['REMOTE_ADDR']
    log.obj_id = obj.id
    log.obj_name = obj.__str__()
    log.save()
