from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import F, Q, When, Case, BooleanField, Value
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models.functions import Concat
from django.core import serializers
from django.forms.models import model_to_dict
from apps.dpv_respuesta.views import *
from .forms import *
from .models import *


@permission_required('dpv_quejas.view_queja', raise_exception=True)
def index(request):
    quejas = Queja.objects.none()
    try:
        perfil = request.user.perfil_usuario
        try:
            ct = perfil.centro_trabajo
            if ct.oc:
                quejas = Queja.objects.all().annotate(radicada=Case(When(id__gt=0, then=True),
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
                    .distinct()
            else:
                quejas = Queja.objects.filter(dir_municipio=ct.municipio,
                                              radicado_por__perfil_usuario__centro_trabajo__municipio=ct.municipio) \
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
                    .distinct()
        except:
            print("no tiene centro de trabajo asociado")
    except:
        print("no tiene perfil asociado")
    return render(request, 'dpv_quejas/list.html', {'quejas': quejas})


@permission_required('dpv_quejas.add_queja', raise_exception=True)
def agregar_queja(request):
    form = QuejaForm(prefix='queja')
    aqform = AQPersonaNaturalForm(prefix='person_procedence', empty_permitted=True, use_required_attribute=False)
    pnform = QPersonaNaturalForm(prefix='person_queja', empty_permitted=True, use_required_attribute=False)
    pjform = QPersonaJuridicaForm(prefix='empresa', empty_permitted=True, use_required_attribute=False)
    tform = QTelefonoForm(prefix='telefono', empty_permitted=True, use_required_attribute=False)
    eform = QEmailForm(prefix='email', empty_permitted=True, use_required_attribute=False)
    orgform = QOrganismoForm(prefix='organismo', empty_permitted=True, use_required_attribute=False)
    oform = QOrganizationForm(prefix='organiza', empty_permitted=True, use_required_attribute=False)
    peform = QPrensaEscritaForm(prefix='pe', empty_permitted=True, use_required_attribute=False)
    person_list = None
    if request.method == "POST":
        form = QuejaForm(request.POST, prefix='queja')
        print('POST Method', request.POST)
        pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', empty_permitted=True,
                                     use_required_attribute=False)
        procedence_form = QAnonimoForm()
        if request.POST.get('pe-nombre'):
            pe = PrensaEscrita.objects.filter(nombre=request.POST.get('pe-nombre'))
            if pe:
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe', use_required_attribute=False,
                                                              instance=pe.first(), empty_permitted=True)
            else:
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe',
                                                              use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('person_procedence-ci') and request.POST.get('person_procedence-nombre'):
            pn = PersonaNatural.objects.filter(ci=request.POST.get('person_procedence-ci'))
            if pn:
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False,
                                                                instance=pn.first(), empty_permitted=True)
            else:
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('telefono-numero'):
            tel = Telefono.objects.filter(numero=request.POST.get('telefono-numero'))
            if tel:
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        instance=tel.first(), empty_permitted=True)
            else:
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        empty_permitted=True)
        elif request.POST.get('email-email'):
            ema = Email.objects.filter(email=request.POST.get('email-email'))
            if ema:
                procedence_form = eform = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     instance=ema.first(), empty_permitted=True)
            else:
                procedence_form = eform = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     empty_permitted=True)
        elif request.POST.get('empresa-nombre') and request.POST.get('empresa-codigo_nit') and request.POST.get(
                'empresa-codigo_reuup'):
            pj = PersonaJuridica.objects.filter(codigo_nit=request.POST.get('empresa-codigo_nit'),
                                                codigo_reuup=request.POST.get('empresa-codigo_reuup'),
                                                nombre=request.POST.get('empresa-nombre'))
            if pj:
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa',
                                                                instance=pj.first(), empty_permitted=True,
                                                                use_required_attribute=False)
            else:
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa', empty_permitted=True,
                                                                use_required_attribute=False)
        elif request.POST.get('organiza-nombre'):
            org = Organizacion.objects.filter(nombre=request.POST.get('organiza-nombre')[0])
            if org:
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza',
                                                            use_required_attribute=False,
                                                            instance=org.first(), empty_permitted=True)
            else:
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza',
                                                            use_required_attribute=False,
                                                            empty_permitted=True)

        if request.POST.get('personas_list'):
            persona_list = request.POST.get('personas_list')
            persona = PersonaNatural.objects.filter(id=persona_list).first()
            # print(model_to_dict(persona))
            if persona:
                pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', instance=persona)
        else:
            persona = PersonaNatural.objects.filter(ci=request.POST.get('person_queja-ci'),
                                                    nombre__iexact=request.POST.get('person_queja-nombre'),
                                                    apellidos__iexact=request.POST.get(
                                                        'person_queja-apellidos')).first()
            if persona:
                pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', instance=persona)

        if form.is_valid() and procedence_form.is_valid() and pnform.is_valid():
            procedence = procedence_form.save()
            if procedence:
                ct = ContentType.objects.get_for_model(procedence)
                proc = Procedencia.objects.create(objecto_contenido=procedence, tipo_contenido=ct,
                                                  id_objecto=procedence.id)
                proc.save_and_log(request=request, af=0)
            else:
                proc, pcreated = Procedencia.objects.get_or_create(nombre="Anónimo",
                                                                   tipo=TipoProcedencia.objects.filter(id=1).first())

            quejoso, qcreated = pnform.Meta.model.objects.get_or_create(nombre=pnform.instance.nombre,
                                                                        ci=pnform.instance.ci,
                                                                        defaults={
                                                                            'apellidos': pnform.instance.apellidos,
                                                                            'telefono': pnform.instance.telefono,
                                                                            'movil': pnform.instance.movil,
                                                                            'email_address': pnform.instance.email_address,
                                                                            'genero': pnform.instance.genero,
                                                                            'direccion_calle': pnform.instance.direccion_calle,
                                                                            'direccion_numero': pnform.instance.direccion_numero,
                                                                            'direccion_entrecalle1': pnform.instance.direccion_entrecalle1,
                                                                            'direccion_entrecalle2': pnform.instance.direccion_entrecalle2,
                                                                            'municipio': pnform.instance.municipio,
                                                                            'cpopular': pnform.instance.cpopular,
                                                                        })
            if qcreated:
                quejoso.save_and_log(request=request, af=0)
            qct = ContentType.objects.get_for_model(quejoso)
            queja = form.save(commit=False)
            queja.procedencia = proc
            queja.radicado_por = request.user
            queja.save_and_log(request=request, af=0)
            damnificado = Damnificado.objects.create(queja=queja, tipo_contenido=qct,
                                                     objecto_contenido=quejoso, id_objecto=quejoso.id)
            damnificado.save_and_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            if request.POST.get('pe-nombre'):
                peform = procedence_form
                peform.initial = model_to_dict(procedence_form.instance)
            elif request.POST.get('person_procedence-ci') and request.POST.get('person_procedence-nombre'):
                aqform = procedence_form
                aqform.initial = model_to_dict(procedence_form.instance)
            elif request.POST.get('telefono-numero'):
                tform = procedence_form
                tform.initial = model_to_dict(procedence_form.instance)
            elif request.POST.get('email-email'):
                eform = procedence_form
                eform.initial = model_to_dict(procedence_form.instance)
            elif request.POST.get('empresa-nombre') and request.POST.get('empresa-codigo_nit') and request.POST.get(
                    'empresa-codigo_reuup'):
                pjform = procedence_form
                pjform.initial = model_to_dict(procedence_form.instance)
            elif request.POST.get('organiza-nombre'):
                oform = procedence_form
                oform.initial = model_to_dict(procedence_form.instance)

            if request.POST.get('personas_list'):
                person_list = request.POST.get('personas_list')
                print(person_list)
            return render(request, 'dpv_quejas/form.html', {'form': form,
                                                            'pnform': pnform,
                                                            'pjform': pjform,
                                                            'tform': tform,
                                                            'eform': eform,
                                                            'orgform': orgform,
                                                            'oform': oform,
                                                            'peform': peform,
                                                            'person_list': person_list,
                                                            'aqform': aqform})
    return render(request, 'dpv_quejas/form.html', {'form': form,
                                                    'pnform': pnform,
                                                    'pjform': pjform,
                                                    'tform': tform,
                                                    'eform': eform,
                                                    'orgform': orgform,
                                                    'oform': oform,
                                                    'peform': peform,
                                                    'person_list': person_list,
                                                    'aqform': aqform})


@permission_required('dpv_quejas.view_queja', raise_exception=True)
def detalle_queja(request, id_queja):
    queja = get_object_or_404(Queja, id=id_queja)
    if request.user.perfil_usuario.centro_trabajo.oc or request.user.perfil_usuario.centro_trabajo.municipio == queja.dir_municipio:
        return render(request, 'dpv_quejas/detail.html', {'queja': queja})
    return HttpResponseForbidden()


@permission_required('dpv_quejas.delete_queja', raise_exception=True)
def eliminar_queja(request, id_queja):
    queja = get_object_or_404(Queja, id=id_queja)
    return render(request, 'dpv_quejas/delete.html', {'queja': queja})


@permission_required('dpv_quejas.add_asignaquejadpto', raise_exception=True)
def asignar_queja_depto(request, id_queja):
    depto = AsignaQuejaDpto()
    depto.quejadpto = Queja.objects.filter(id=id_queja).first()
    form = AsignaQuejaDptoForm(instance=depto)
    if request.method == 'POST':
        form = AsignaQuejaDptoForm(request.POST, instance=depto)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            return render(request, 'dpv_quejas/asignar_depto.html', {'form': form})
    else:
        return render(request, 'dpv_quejas/asignar_depto.html', {'form': form, 'queja': id_queja})


@permission_required('dpv_quejas.add_asignaquejatecnico', raise_exception=True)
def asignar_queja_tecnico(request, id_queja):
    tecnico = AsignaQuejaTecnico()
    tecnico.quejatecnico = get_object_or_404(Queja, id=id_queja)
    form = AsignaQuejaTecnicoForm(instance=tecnico)
    if request.method == 'POST':
        form = AsignaQuejaTecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form})
    tecs = Tecnico.objects.filter(profile__depto_trabajo=request.user.perfil_usuario.depto_trabajo,
                                  profile__centro_trabajo=request.user.perfil_usuario.centro_trabajo)
    return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form, 'queja': id_queja, 'tecs': tecs})


def responder_queja(request, id_queja):
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
    messages.warning(request, "Puede existir un error del sistema pero al parecer está intentando responder una queja que no le ha sido asignada")
    return redirect(reverse_lazy("quejas_list"))


def aprobar_respuesta_tecnico(request, id_queja):
    return render(request, 'dpv_quejas/jefe_aprueba.html')


def aprobar_respuesta_depto(request, id_queja):
    return render(request, 'dpv_quejas/director_aprueba.html')


def notificar_respuesta_queja(request, id_queja):
    return render(request, 'dpv_quejas/notificacion.html')


def rechazar_queja(request, id_queja):
    return render(request, 'dpv_quejas/rechazada.html')


def redirigir_queja(request, id_queja):
    return render(request, 'dpv_quejas/redirigida.html')


class AprobadaRespuestaQuejaDtorView(AprobadaRespuestaDtorView):
    success_url = reverse_lazy('quejas_list')

    def get_context_data(self, **kwargs):
        context = super(AprobadaRespuestaQuejaDtorView, self).get_context_data(**kwargs)
        print(kwargs)
        # context['']

        return context


class AprobadaRespuestaQuejaJefeView(AprobadaRespuestaJefeView):
    success_url = reverse_lazy('quejas_list')
