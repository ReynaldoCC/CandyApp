from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q, When, Case, BooleanField, Count, F, Value, PositiveIntegerField, CharField
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from apps.dpv_respuesta.forms import ApruebaDtrForm, ApruebaJefeForm, RespuestaRechazadaForm

from .forms import *
from .models import *
from .tasks import notify_queja
from .decorators import some_permission_required

DEFAULT_SHOW_ITEMS = 20


@some_permission_required(('dpv_quejas.view_queja',
                           'dpv_quejas.view_asignaquejatecnico',
                           'dpv_quejas.view_respuestaqueja',), raise_exception=True)
def index(request):
    """
    Funcion de index de quejas, esta vista muestra las quejas en dependencia de los los permisos del usuario y el centro
    de trabajo que el usuario tiene configurado en el perfil. Segun el centro de trabajo el usuario podra, si el centro
    de trabajo es OC, ver todas las quejas de las unidades de dicho centro de trabajo, si el centro de trabajo no es OC
    entonces solo podra ver las quejas de su centro de trabajo. Segun los permisos asignado al usuario el usuario podra:
        - 'view_queja': visualizar todas las quejas
        - 'view_asignaquejatecnico': visualizar todas las asignadas al departamento al que pertence el usuario segun su
        perfil.
        - 'view_respuestaqueja': visualizar solo las quejas a le han sido asignadas para dar su respuesta

    :param request: objeto request
    :return:
    """
    quejas = Queja.objects.none()
    try:
        perfil = request.user.perfil_usuario
        try:
            ct = perfil.centro_trabajo
            ver_quejas_query = Q(id__isnull=False)
            if request.user.has_perm('dpv_quejas.view_respuestaqueja'):
                ver_quejas_query = Q(quejatecnico__tecnico__profile__datos_usuario__id=request.user.id)
            if request.user.has_perm('dpv_quejas.view_asignaquejatecnico'):
                ver_quejas_query = Q(quejadpto__dpto__id=request.user.perfil_usuario.depto_trabajo.id)
            if request.user.has_perm('dpv_quejas.view_queja'):
                ver_quejas_query = Q(id__isnull=False)
            if ct.oc:
                quejas = Queja.objects.filter(ver_quejas_query) \
                    .annotate(radicada=Case(When(id__gt=0, then=True),
                                            default=False,
                                            output_field=BooleanField()),
                              asignada_depto=Case(When(
                                  Q(quejadpto__id__gt=0, quejadpto__rechazada__isnull=True),
                                  then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              asignada_tecnico=Case(When(Q(quejatecnico__id__gt=0,
                                                           quejatecnico__rechazada__isnull=True),
                                                         then=True),
                                                    default=False,
                                                    output_field=BooleanField()),
                              respondida=Case(When(
                                  Q(respuesta__id__gt=0, respuesta__rechazada__isnull=True),
                                  then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              aprobada_depto=Case(When(Q(respuesta__apruebajefe__id__gt=0,
                                                         respuesta__apruebajefe__isnull=False),
                                                       then=True),
                                                  default=False,
                                                  output_field=BooleanField()),
                              aprobada_dir=Case(When(
                                  Q(respuesta__id__gt=0, respuesta__apruebadtr__gt=0,
                                    respuesta__apruebadtr__isnull=False), then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              ) \
                    .distinct("id")
            else:
                quejas = Queja.objects.filter(dir_municipio=ct.municipio,
                                              radicado_por__perfil_usuario__centro_trabajo__municipio=ct.municipio) \
                    .filter(ver_quejas_query) \
                    .annotate(radicada=Case(When(id__gt=0, then=True),
                                            default=False,
                                            output_field=BooleanField()),
                              asignada_depto=Case(
                                  When(Q(quejadpto__id__gt=0, quejadpto__rechazada__isnull=True), then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              asignada_tecnico=Case(
                                  When(Q(quejatecnico__id__gt=0, quejatecnico__rechazada__isnull=True), then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              respondida=Case(
                                  When(Q(respuesta__id__gt=0, respuesta__rechazada__isnull=True), then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              aprobada_depto=Case(
                                  When(Q(respuesta__apruebajefe__id__gt=0, respuesta__apruebajefe__isnull=False),
                                       then=True),
                                  default=False,
                                  output_field=BooleanField()),
                              aprobada_dir=Case(When(Q(respuesta__id__gt=0, respuesta__apruebadtr__gt=0,
                                                       respuesta__apruebadtr__isnull=False), then=True),
                                                default=False,
                                                output_field=BooleanField()),
                              ) \
                    .distinct("id")
        except ObjectDoesNotExist:
            messages.warning(request,
                             """No se mostraran las quejas ya que el usuario no tiene centro de trabajo asociado, si 
                             cree que es un error contacte con la administración del sistema""")
    except ObjectDoesNotExist:
        messages.warning(request,
                         """No se mostraran las quejas ya que el usuario no tiene perfil asociado, si cree que 
                         es un error contacte con la administración del sistema""")
    return render(request, 'dpv_quejas/list.html', {'quejas': quejas})


@permission_required('dpv_quejas.add_queja', raise_exception=True)
def agregar_queja(request):
    """
    Funcion de vista para agregar quejas.
    :param request: objeto request
    :return:
    """
    form = QuejaForm(prefix='queja')
    if request.method == "POST":
        form = QuejaForm(request.POST, request.FILES, prefix='queja')
        if form.is_valid():
            queja = form.save(commit=False)
            queja.radicado_por = request.user
            queja.save_and_log(request=request, af=0)
            messages.success(request, _("Queja " + queja.__str__() + " agregada satisfactoriamente"))
            return redirect(reverse_lazy('quejas_list'))
        else:
            messages.error(request, _("No se ha podido agregar la queja"))
            return render(request, 'dpv_quejas/form.html', {'form': form})
    return render(request, 'dpv_quejas/form.html', {'form': form})


@permission_required('dpv_quejas.view_queja', raise_exception=True)
def detalle_queja(request, id_queja):
    """
    Funcion de vista para visualizar los detalles de una queja
    :param request: objeto request
    :param id_queja: Entero PK de la queja que se quiere ver el detalle
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    if request.user.perfil_usuario.centro_trabajo.oc or \
            request.user.perfil_usuario.centro_trabajo.municipio == queja.dir_municipio:
        return render(request, 'dpv_quejas/detail.html', {'queja': queja})
    return HttpResponseForbidden()


@permission_required('dpv_quejas.delete_queja', raise_exception=True)
def eliminar_queja(request, id_queja):
    """
    Funcion de vista para eliminar una queja
    :param request: objeto request
    :param id_queja: Entero PK de la queja que se quiere eliminar
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    return render(request, 'dpv_quejas/delete.html', {'queja': queja})


@permission_required('dpv_quejas.add_asignaquejadpto', raise_exception=True)
def asignar_queja_depto(request, id_queja):
    """
    Funcion de vista para asignar una queja a un departamento para que sea dada respuesta a la queja
    :param request: objeto request
    :param id_queja: Entero PK de la queja que se quiere asignar al departamento
    :return:
    """
    depto = AsignaQuejaDpto()
    depto.quejadpto = Queja.objects.filter(id=id_queja).first()
    form = AsignaQuejaDptoForm(instance=depto)
    if request.method == 'POST':
        form = AsignaQuejaDptoForm(request.POST, instance=depto)
        if form.is_valid():
            model = form.save(commit=False)
            model.asignador = request.user
            model.save_and_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            return render(request, 'dpv_quejas/asignar_depto.html', {'form': form})
    else:
        return render(request, 'dpv_quejas/asignar_depto.html', {'form': form, 'queja': id_queja})


@permission_required('dpv_quejas.add_asignaquejatecnico', raise_exception=True)
def asignar_queja_tecnico(request, id_queja):
    """
    Funcion de vista para asignar una queja a un tecnico
    :param request: objeto request
    :param id_queja: Entero PK de la queja que se quiere asignar al tecnico
    :return:
    """
    tecnico = AsignaQuejaTecnico()
    tecnico.quejatecnico = get_object_or_404(Queja, id=id_queja)
    form = AsignaQuejaTecnicoForm(instance=tecnico)
    if request.method == 'POST':
        form = AsignaQuejaTecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            model = form.save(commit=False)
            model.asignador = request.user
            model.save_and_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form})
    tecs = Tecnico.objects.filter(profile__depto_trabajo=request.user.perfil_usuario.depto_trabajo,
                                  profile__centro_trabajo=request.user.perfil_usuario.centro_trabajo)
    return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form, 'queja': id_queja, 'tecs': tecs})


@permission_required('dpv_quejas.add_respuestaqueja', raise_exception=True)
def responder_queja(request, id_queja):
    """
    Funcion de vista para dar respuesta a una queja, esta funcion valida que el usuario que quiere dar respuesta a la
    queja es el mismo al que se le ha asignado la queja para dar respuesta
    :param request: objeto request
    :param id_queja: Entero PK de la queja que se quiere dar respuesta
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    if request.user and queja.get_tecnico_asignado:
        if request.user != queja.get_tecnico_asignado.profile.datos_usuario:
            return HttpResponseForbidden()
        respuesta = RespuestaQueja()
        respuesta.queja = queja
        form = QRespuestaForm(instance=respuesta)
        if request.method == "POST":
            form = QRespuestaForm(request.POST, instance=respuesta)
            if form.is_valid():
                respuesta = form.save(commit=False)
                respuesta.responde = request.user.perfil_usuario.tecnico.first()
                respuesta.save_and_log(request=request, af=0)
                messages.success(request=request, message="Respuesta de la queja guardada satisfacoriamente")
                return redirect(reverse_lazy("quejas_list"))
            else:
                messages.success(request=request,
                                 message="Existen errores en el fomrulario de respuesta por lo que no se pudo guardar.")
        return render(request, 'dpv_quejas/response_form.html', {"form": form, "queja": queja})
    messages.warning(request,
                     """Puede existir un error del sistema pero al parecer está intentando 
                     responder una queja que no le ha sido asignada""")
    return redirect(reverse_lazy("quejas_list"))


@permission_required('dpv_respuesta.add_apruebajefe', raise_exception=True)
def aprobar_respuesta_tecnico(request, id_queja):
    """
    Funcion de vista para aprobar una respuesta a una queja dada por un tecnico, esta funcion otorga un primer nivel de
    aprbacion de la respuesta, son necesarios 2 niveles de aprobacion.
    :param request:
    :param id_queja: Entero PK de la queja  que tiene la respuesta que se quiere aprobar
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    form = ApruebaJefeForm()
    reject_form = RespuestaRechazadaForm()
    if request.method == 'POST':
        form = ApruebaJefeForm(request.POST)
        if form.is_valid():
            aprobado = form.save(commit=False)
            aprobado.fecha_jefe = timezone.now()
            aprobado.respuesta = queja.get_respuesta
            aprobado.aprobada_por = request.user.perfil_usuario
            aprobado.save_and_log(request=request, af=0)
            messages.success(request, "Respuesta a queja aprobada satisfactoriamente")
            return redirect(reverse_lazy("quejas_list"))
        else:
            messages.error(request, "existen errores en el formulario")
    return render(request, 'dpv_quejas/jefe_aprueba.html', {"queja": queja,
                                                            "form": form,
                                                            "reject_form": reject_form})


@permission_required('dpv_respuesta.add_apruebadtr', raise_exception=True)
def aprobar_respuesta_depto(request, id_queja):
    """
    Funcion de vista para aprobar una respuesta a una queja dada por un tecnico y revisada y aprobada por un usuario
    jefe de depto, esta funcion otorga el segundo nivel de aprobacion de la respuesta, son necesarios 2 niveles de
    aprobacion.
    :param request: objeto request
    :param id_queja: Entero PK de la queja  que tiene la respuesta que se quiere aprobar
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    form = ApruebaDtrForm()
    reject_form = RespuestaRechazadaForm()
    if request.method == "POST":
        form = ApruebaDtrForm(request.POST)
        if form.is_valid():
            aprobadr = form.save(commit=False)
            aprobadr.fecha_dtr = timezone.now()
            aprobadr.aprobada_por = request.user.perfil_usuario
            aprobadr.respuesta = queja.get_respuesta
            aprobadr.save_and_log(request=request, af=0)
            messages.success(request, "Respuesta a queja aprobada satisfactoriamente")
            return redirect(reverse_lazy("quejas_list"))
        else:
            messages.error(request, "exiten errores en el formulario")
    return render(request, 'dpv_quejas/director_aprueba.html', {"queja": queja,
                                                                "form": form,
                                                                "reject_form": reject_form})


@permission_required('dpv_quejas.add_quejanotificada', raise_exception=True)
def notificar_respuesta_queja(request, id_queja):
    """
    Funcion de vista para aprobar una respuesta a una queja dada por un tecnico, esta funcion otorga un primer nivel de
    aprbacion de la respuesta, son necesarios 2 niveles de aprobacion.
    :param request: objeto request
    :param id_queja: Entero PK de la queja  que tiene la respuesta que se quiere aprobar
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    notify_queja.delay(queja.id)
    return render(request, 'dpv_quejas/notificacion.html')


@permission_required('dpv_quejas.add_rechazada', raise_exception=True)
def rechazar_queja(request, id_queja, level):
    """
    Funcion de vista para rechazar una respuesta dada
    :param request: objeto request
    :param id_queja: Entero PK de la queja  que tiene la respuesta que se quiere rechazar
    :return:
    """
    queja = get_object_or_404(Queja, id=id_queja)
    form = ApruebaJefeForm()
    reject_form = RespuestaRechazadaForm()
    if request.method == "POST":
        reject_form = RespuestaRechazadaForm(request.POST)
        if reject_form.is_valid():
            rechazada = reject_form.save(commit=False)
            rechazada.respuesta = queja.get_respuesta
            rechazada.rechazador = request.user
            rechazada.nivel = int(level)
            rechazada.save()
            if rechazada:
                respuesta = queja.get_respuesta
                respuesta.rechazada = rechazada.created_at
                respuesta.save_and_log(request=request, af=1)
                messages.info(request, "Respuesta a queja ha sido rechazada")
            return redirect(reverse_lazy("quejas_list"))

    return render(request, 'dpv_quejas/rechazada.html', {"reject_form": reject_form,
                                                         "form": form,
                                                         "queja": queja})


@permission_required('dpv_quejas.add_redirigida', raise_exception=True)
def redirigir_queja(request, id_queja):
    queja = get_object_or_404(Queja, id=id_queja)
    return render(request, 'dpv_quejas/redirigida.html', {"queja": queja})


@some_permission_required(('dpv_quejas.view_queja',
                           'dpv_quejas.view_asignaquejatecnico',
                           'dpv_quejas.view_respuestaqueja',), raise_exception=True)
def historia_queja(request, id_queja):
    queja = get_object_or_404(Queja, id=id_queja)
    items = [{"tipo": "queja", "fecha": queja.created_at, "objeto": queja}]
    for item in queja.quejadpto.all():
        items.append({"tipo": "asignadepto", "fecha": item.fecha_asignacion, "objeto": item})
    for item in queja.quejatecnico.all():
        items.append({"tipo": "asignatecnico", "fecha": item.fecha_asignacion, "objeto": item})
    for item in queja.respuesta.all():
        items.append({"tipo": "respuesta", "fecha": item.fecha_respuesta, "objeto": item})
        for subitem in item.apruebajefe_set.all():
            items.append({"tipo": "apruebajefe", "fecha": subitem.fecha_jefe, "objeto": subitem})
        for subitem in item.apruebadtr_set.all():
            items.append({"tipo": "apruebadtr", "fecha": subitem.fecha_dtr, "objeto": subitem})
        for subitem in item.respuestarechazada_set.all():
            items.append({"tipo": "respuestarechazada", "fecha": subitem.fecha_rechazada, "objeto": subitem})
    for item in queja.notificada.all():
        items.append({"tipo": "quejanotificada", "fecha": item.fecha, "objeto": item})
    items.sort(key=lambda u: u["fecha"])
    return render(request, 'dpv_quejas/history.html', {"items": items, "queja": queja})


@permission_required('dpv_quejas.view_queja', raise_exception=True)
def stats_queja(request):
    """
    View function to show general statistic about quejas
    :param request: Request object
    :return: A View
    """
    today = datetime.datetime.now()
    if request.user.perfil_usuario.centro_trabajo.oc:
        result = [queja for queja in Queja.objects
            .values('dir_municipio__nombre', 'dir_municipio__id')
            .annotate(asignadadpto=Count('quejadpto', distinct=True),
                      asignadatec=Count('quejatecnico', distinct=True),
                      quejarechaza=Count('rechazada', distinct=True),
                      quejaredirige=Count('redirigida', distinct=True),
                      quejarespondida=Count(Case(When(Q(respuesta__id__isnull=False,
                                                        respuesta__rechazada__isnull=True),
                                                      then=F('id')),
                                                 default=Value(None),
                                                 output_field=PositiveIntegerField()), distinct=True),
                      aprobada_jefe=Count(Case(When(Q(respuesta__id__isnull=False,
                                                      respuesta__rechazada__isnull=True,
                                                      respuesta__apruebajefe__isnull=False),
                                                    then=F('id')),
                                               default=Value(None),
                                               output_field=PositiveIntegerField()), distinct=True),
                      aprobada_dtr=Count(Case(When(Q(respuesta__id__isnull=False,
                                                     respuesta__rechazada__isnull=True,
                                                     respuesta__apruebadtr__isnull=False),
                                                   then=F('id')),
                                              default=Value(None),
                                              output_field=PositiveIntegerField()), distinct=True),
                      menos_30d=Count(Case(When(Q(fecha_radicacion__gt=(today - datetime.timedelta(days=30))),
                                                then=F('id')),
                                           default=Value(None),
                                           output_field=PositiveIntegerField()), distinct=True),
                      between_30d_60d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=30)),
                                                        fecha_radicacion__gte=(today - datetime.timedelta(days=60))),
                                                      then=F('id')),
                                                 default=Value(None),
                                                 output_field=PositiveIntegerField()), distinct=True),
                      between_60d_90d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=60)),
                                                        fecha_radicacion__gte=(today - datetime.timedelta(days=90))),
                                                      then=F('id')),
                                                 default=Value(None),
                                                 output_field=PositiveIntegerField()), distinct=True),
                      older_90d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=90))),
                                                then=F('id')),
                                           default=Value(None),
                                           output_field=PositiveIntegerField()), distinct=True),
                      quejanotificada=Count('notificada'),
                      type=Value('municipio', output_field=CharField()),
                      cantquejas=Count('id', distinct=True))]
    else:
        return redirect(reverse_lazy('quejas_stats',
                                     kwargs={'id_municipio': request.user.perfil_usuario.centro_trabajo.municipio.id}))
    return render(request, 'dpv_quejas/estadistico.html', {'result': result})


@permission_required('dpv_quejas.view_queja', raise_exception=True)
def stats_queja_municipal(request, id_municipio):
    """
    View function to show general statistic about quejas of especific municipality
    :param id_municipio: Int PK of municipality to get quejas about
    :param request: Request object
    :return: A View
    """
    today = datetime.datetime.now()
    result = [queja for queja in Queja.objects.filter(dir_municipio__id=id_municipio)
        .values('dir_cpopular__nombre', 'dir_cpopular__id')
        .annotate(asignadadpto=Count('quejadpto', distinct=True),
                  asignadatec=Count('quejatecnico', distinct=True),
                  quejarechaza=Count('rechazada', distinct=True),
                  quejaredirige=Count('redirigida', distinct=True),
                  quejarespondida=Count(Case(When(Q(respuesta__id__isnull=False,
                                                    respuesta__rechazada__isnull=True),
                                                  then=F('id')),
                                             default=Value(None),
                                             output_field=PositiveIntegerField()), distinct=True),
                  aprobada_jefe=Count(Case(When(Q(respuesta__id__isnull=False,
                                                  respuesta__rechazada__isnull=True,
                                                  respuesta__apruebajefe__isnull=False),
                                                then=F('id')),
                                           default=Value(None),
                                           output_field=PositiveIntegerField()), distinct=True),
                  aprobada_dtr=Count(Case(When(Q(respuesta__id__isnull=False,
                                                 respuesta__rechazada__isnull=True,
                                                 respuesta__apruebadtr__isnull=False),
                                               then=F('id')),
                                          default=Value(None),
                                          output_field=PositiveIntegerField()), distinct=True),
                  menos_30d=Count(Case(When(Q(fecha_radicacion__gt=(today - datetime.timedelta(days=30))),
                                            then=F('id')),
                                       default=Value(None),
                                       output_field=PositiveIntegerField()), distinct=True),
                  between_30d_60d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=30)),
                                                    fecha_radicacion__gte=(today - datetime.timedelta(days=60))),
                                                  then=F('id')),
                                             default=Value(None),
                                             output_field=PositiveIntegerField()), distinct=True),
                  between_60d_90d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=60)),
                                                    fecha_radicacion__gte=(today - datetime.timedelta(days=90))),
                                                  then=F('id')),
                                             default=Value(None),
                                             output_field=PositiveIntegerField()), distinct=True),
                  older_90d=Count(Case(When(Q(fecha_radicacion__lt=(today - datetime.timedelta(days=90))),
                                            then=F('id')),
                                       default=Value(None),
                                       output_field=PositiveIntegerField()), distinct=True),
                  quejanotificada=Count('notificada'),
                  type=Value('cpopular', output_field=CharField()),
                  municipio=F('dir_municipio__id'),
                  cantquejas=Count('id', distinct=True))]
    return render(request, 'dpv_quejas/estadistico.html', {'result': result})


@permission_required('dpv_quejas.view_damnificado', raise_exception=True)
def list_damnificado(request):
    """
    View function to show the the list of damnificados of quejas paginated
    :param request: Request object
    :return: A View
    """
    page = request.GET.get('page', 1)
    search = request.GET.get('search', "")
    if search is not None and search != "":
        # TODO make query to search over nombre, apellidos and other fields of damnificado
        damnificado_list = Damnificado.objects.all()
    else:
        damnificado_list = Damnificado.objects.all()

    paginator = Paginator(damnificado_list, DEFAULT_SHOW_ITEMS)
    try:
        damnificados = paginator.page(page)
    except PageNotAnInteger:
        damnificados = paginator.page(1)
    except EmptyPage:
        damnificados = paginator.page(paginator.num_pages)

    return render(request, 'dpv_quejas/damnificado/list.html', {'damnificados': damnificados})


@permission_required('dpv_quejas.add_damnificado', raise_exception=True)
def add_damnificado(request):
    """
    View function to add new damnificado to the list of damnificados, this function take three forms to evaluate they
    and save a new instance of damnificado
    :param request: Request object
    :return: [A View, Redierct, JsonResponse]A VIew or Redirect if request is POST or JsonResponse if request is Ajax
    """
    damn_form = DamnificadoAddForm()
    pnform = PersonaNaturalForm(prefix='pn', empty_permitted=True, use_required_attribute=False)
    pjform = PersonaJuridicaForm(prefix='pj', empty_permitted=True, use_required_attribute=False)
    if request.method == "POST":
        data = dict()
        damn_form = DamnificadoAddForm(request.POST)
        if damn_form.is_valid():
            objeto_contenido = None
            damn = damn_form.save(commit=False)
            if damn.tipo_contenido.model.lower() == "personanatural":
                if damn_form.cleaned_data.get('personas'):
                    objeto_contenido = damn_form.cleaned_data.get('personas')
                else:
                    pnform = PersonaNaturalForm(request.POST,
                                                prefix='pn',
                                                empty_permitted=True,
                                                use_required_attribute=False)
                    if pnform.is_valid():
                        objeto_contenido = pnform.save()
            elif damn.tipo_contenido.model.lower() == "personajuridica":
                if damn_form.cleaned_data.get('empresas'):
                    objeto_contenido = damn_form.cleaned_data.get('empresas')
                else:
                    pjform = PersonaJuridicaForm(request.POST,
                                                 prefix='pj',
                                                 empty_permitted=True,
                                                 use_required_attribute=False)
                    if pjform.is_valid():
                        objeto_contenido = pjform.save()
            else:
                objeto_contenido = None
            if objeto_contenido is not None and damn.tipo_contenido is not None:
                damn.objecto_contenido = objeto_contenido
                damn.id_objecto = objeto_contenido.id
                damn.save()
                if request.is_ajax():
                    data = model_to_dict(damn)
                    data["objecto_contenido"] = model_to_dict(damn.objecto_contenido)
                    data["nombre"] = damn.__str__()
                    data["message"] = _("Damnificado agregado satisfactoriamente")
                    return JsonResponse(data=data, status=201)
                else:
                    messages.success(request, _("Damnificado agregado satisfactoriamente"))
                    return redirect(reverse_lazy("quejas_damnificados"))
            else:
                if request.is_ajax():
                    data["message"] = _("No es ha podido agregar el damnificado porque no es del tipo correcto")
                    return JsonResponse(data=data, status=400)
                else:
                    messages.success(request,
                                     _("No es ha podido agregar el damnificado porque no es del tipo correcto"))
                    return redirect(reverse_lazy("quejas_damnificados"))
        else:
            if request.is_ajax():
                data['errors'] = dict(dict(damn_form.errors),
                                      **dict(pnform.errors),
                                      **dict(pjform.errors))
                status = 400
                return JsonResponse(data=data, status=status)
            else:
                messages.success(request,
                                 _("Errores en el formualrio"))
                return redirect(reverse_lazy("quejas_damnificados"))
    return render(request, 'dpv_quejas/damnificado/add_form.html', {"damn_form": damn_form,
                                                                    "pnform": pnform,
                                                                    "pjform": pjform})


@permission_required('dpv_quejas.view_damnificado', raise_exception=True)
def get_damnificado_detail(request, id_damn):
    """
    View function to get detail about damnificado object, this function take id of damnificado and return the detail of
    object founded in json or template depending of request type
    :param request: Request object
    :param id_damn: Int PK of damnificado to get details
    :return: [A View, JsonResponse] A View or JsonResponse if request is ajax.
    """
    damn = get_object_or_404(Damnificado, id=id_damn)
    if request.is_ajax():
        data_damn = model_to_dict(damn)
        data_damn["nombre"] = damn.__str__()
        data_damn["objecto_contenido"] = model_to_dict(damn.objecto_contenido)
        return JsonResponse(data=data_damn, status=200)
    else:
        return render(request, "dpv_quejas/damnificado/detail.html", {"damnificado": damn})


@login_required
def get_damnificados_json(request):
    """
    View function to get the list of damnificados in json with values of id, and nombre, who nombre is the return of
    __str__ method, used for selects.
    :param request: Request object
    :return: JsonResponse
    """
    # TODO Make the query inside db server and not python treatment
    damnificados = list({"id": damn.id, "nombre": damn.__str__()} for damn in Damnificado.objects.all())
    return JsonResponse(data=damnificados, safe=False, status=200)
