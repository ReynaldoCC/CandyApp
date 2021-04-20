from django.db.models import Count, Q
from django.utils.text import Truncator
from apps.dpv_nomencladores.models import Procedencia
from apps.dpv_documento.models import TipoDPVDocumento, DPVDocumento
import datetime


def resume_first_targets(request):

    targets = list()

    targets.append({
        "title": "Members online",
        "total": 584,
        "color": 1,
        "data": {
            "labels": ['Enero', 'Febrero', 'Marzo', 'Abril'],
            "type": 'line',
            "datasets": {
                "data": [65, 59, 84, 84],
                "label": "Total"
            }
        }
    })

    targets.append({
        "title": "Members online",
        "total": 45,
        "color": 2,
        "data": {
            "labels": ['Enero', 'Febrero', 'Marzo', 'Abril'],
            "type": 'line',
            "datasets": {
                "data": [1, 18, 9, 17],
                "label": "Total"
            }
        }
    })

    targets.append({
        "title": "Members online",
        "total": 284,
        "color": 3,
        "data": {
            "labels": ['Enero', 'Febrero', 'Marzo', 'Abril'],
            "type": 'line',
            "datasets": {
                "data": [78, 81, 80, 45],
                "label": "Total"
            }
        }
    })

    targets.append({
        "title": "Members online",
        "total": 196,
        "color": 4,
        "data": {
            "labels": ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
            "type": 'line',
            "datasets": {
                "data": [27, 55, 47, 67, 26],
                "label": "Total"
            }
        }
    })

    return targets


def resume_second_targets(request):

    targets = list()

    targets.append({
        "title": "Clasificaciones",
        "total": len(TipoDPVDocumento.objects.filter(dpvdocumento__isnull=False).distinct()),
        "color": "success",
        "icon": "envelope"
    })
    targets.append({
        "title": "Documentos",
        "total": len(DPVDocumento.objects.all()),
        "color": "primary",
        "icon": "archive"
    })
    targets.append({
        "title": "Procedencias",
        "total": len(Procedencia.objects.filter(dpvdocumento__isnull=False).distinct()),
        "color": "warning",
        "icon": "layout-grid2"
    })

    return targets


def resume_documents_by_classification(request):
    data = list()

    [data.append({
        "title": "{name}".format(name=Truncator(type_doc.nombre.upper()).chars(30)),
        "value": len(DPVDocumento.objects.filter(clasificacion_id__exact=type_doc.id))
    }) for type_doc in TipoDPVDocumento.objects.filter(dpvdocumento__isnull=False).distinct()]

    return data


def resume_documents_by_origin(request):
    data = list()

    [data.append({
        "title": "{name}".format(name=Truncator(origin.nombre.upper()).chars(30)),
        "value": len(DPVDocumento.objects.filter(procedencia_id__exact=origin.id))
    }) for origin in Procedencia.objects.filter(dpvdocumento__isnull=False).annotate(
        count=Count(Q(dpvdocumento__isnull=False))
    ).order_by('-count', 'nombre')[:5]]

    return data


def resume_documents_with_answers(request):
    data = list()

    return data


def resume_documents_in_time(request):
    data = list()

    [data.append({
        "title": "{name}".format(name=Truncator(query['title'].upper()).chars(30)),
        "value": len(DPVDocumento.objects.filter(query['consult']))
    }) for query in ({'title': 'EN TIEMPO', 'consult': Q(fecha_termino__gte=datetime.datetime.now())}, {'title': 'FUERA DE FECHA', 'consult': Q(fecha_termino__lt=datetime.datetime.now())})]

    return data
