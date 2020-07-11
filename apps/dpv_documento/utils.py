from django.utils import timezone


# Utils functionalities
def configurar_numero_registro(instancia=None, sender=None):
    if instancia and instancia.id:
        ultimo_doc = sender.objects.exclude(id=instancia.id)\
            .filter(fecha_registro__year=timezone.now().year).order_by('fecha_registro').last()
    else:
        ultimo_doc = sender.objects.filter(fecha_registro__year=timezone.now().year).order_by('fecha_registro').last()
    if ultimo_doc:
        ultimo_numero = ultimo_doc.no_registro
        if len(ultimo_numero) < 11:
            if len(ultimo_numero) == 10:
                try:
                    consecutivo = str(int(ultimo_numero[10:])+1).zfill(4)
                except:
                    consecutivo = '0001'
            else:
                try:
                    consecutivo = str(int(ultimo_doc.numero[6:])+1).zfill(4)
                except:
                    consecutivo = '0001'
                # revisar a partir de que pardete del codigo falla
        elif len(ultimo_numero) < 10:
            consecutivo = str(int(ultimo_numero[6:])+1).zfill(4)
        else:
            consecutivo = str(int(ultimo_numero[-4:])+1).zfill(4)

        instancia.no_registro = '%s%s%s%s' % (timezone.now().strftime('%y'),
                                              timezone.now().strftime('%m'),
                                              timezone.now().strftime('%d'),
                                              consecutivo)
    else:
        instancia.no_registro = '%s%s%s%s' % (timezone.now().strftime('%y'),
                                              timezone.now().strftime('%m'),
                                              timezone.now().strftime('%d'),
                                              '0001')
