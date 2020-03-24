from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import F, Q, When, Case, BooleanField, Value
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
                                                      asignada_depto=Case(When(quejadpto__rechazada__isnull=True, then=True),
                                                                          default=False,
                                                                          output_field=BooleanField()),
                                                      asignada_tecnico=Case(When(quejatecnico__rechazada__isnull=True, then=True),
                                                                            default=False,
                                                                            output_field=BooleanField()),
                                                      respondida=Case(When(respuesta__rechazada__isnull=True, then=True),
                                                                      default=False,
                                                                      output_field=BooleanField()),
                                                      aprobada_depto=Case(When(respuesta__apruebajefe__isnull=False, then=True),
                                                                          default=False,
                                                                          output_field=BooleanField()),
                                                      aprobada_dir=Case(When(respuesta__apruebadtr__isnull=False, then=True),
                                                                        default=False,
                                                                        output_field=BooleanField()),
                                                      )\
                                            .distinct()
            else:
                quejas = Queja.objects.filter(dir_municipio=ct.municipio,
                                              radicado_por__perfil_usuario__centro_trabajo__municipio=ct.municipio)\
                                      .annotate(radicada=Case(When(id__gt=0, then=True),
                                                              default=False,
                                                              output_field=BooleanField()),
                                                asignada_depto=Case(When(quejadpto__rechazada__isnull=True, then=True),
                                                                    default=False,
                                                                    output_field=BooleanField()),
                                                asignada_tecnico=Case(When(quejatecnico__rechazada__isnull=True, then=True),
                                                                      default=False,
                                                                      output_field=BooleanField()),
                                                respondida=Case(When(respuesta__rechazada__isnull=True, then=True),
                                                                default=False,
                                                                output_field=BooleanField()),
                                                aprobada_depto=Case(When(respuesta__apruebajefe__isnull=False, then=True),
                                                                    default=False,
                                                                    output_field=BooleanField()),
                                                aprobada_dir=Case(When(respuesta__apruebadtr__isnull=False, then=True),
                                                                  default=False,
                                                                  output_field=BooleanField()),
                                                )\
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
    gform = QGobiernoForm(prefix='gob', empty_permitted=True, use_required_attribute=False)
    if request.method == "POST":
        form = QuejaForm(request.POST, prefix='queja')
        print('POST Method', request.POST)
        pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', empty_permitted=True, use_required_attribute=False)
        procedence_form = QAnonimoForm()
        if request.POST.get('pe-nombre'):
            print('formulario procedencia pe detectado')
            pe = PrensaEscrita.objects.filter(nombre=request.POST.get('pe-nombre'))
            if pe:
                print('instancia de formulario procedencia pe detectado')
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe', use_required_attribute=False,
                                                              instance=pe.first(), empty_permitted=True)
            else:
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe',
                                                              use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('person_procedence-ci') and request.POST.get('person_procedence-nombre'):
            print('formulario procedencia persona detectado')
            pn = PersonaNatural.objects.filter(ci=request.POST.get('person_procedence-ci'))
            if pn:
                print('instancia de formulario procedencia persona detectado')
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence', use_required_attribute=False,
                                                                instance=pn.first(), empty_permitted=True)
            else:
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('telefono-numero'):
            print('formulario procedencia telefono detectado')
            tel = Telefono.objects.filter(numero=request.POST.get('telefono-numero'))
            if tel:
                print('instancia de formulario procedencia telefono detectado')
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        instance=tel.first(), empty_permitted=True)
            else:
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        empty_permitted=True)
        elif request.POST.get('email-email'):
            print('formulario procedencia email detectado')
            ema = Email.objects.filter(email=request.POST.get('email-email'))
            if ema:
                print('instancia de formulario procedencia email detectado')
                procedence_form = eform = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     instance=ema.first(), empty_permitted=True)
            else:
                procedence_form = eform = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     empty_permitted=True)
        elif request.POST.get('empresa-nombre') and request.POST.get('empresa-codigo_nit') and request.POST.get('empresa-codigo_reuup'):
            print('formulario procedencia empresa detectado', request.POST.get('empresa-codigo_nit'), request.POST.get('empresa-codigo_reuup'), request.POST.get('empresa-nombre'))
            pj = PersonaJuridica.objects.filter(codigo_nit=request.POST.get('empresa-codigo_nit'),
                                                codigo_reuup=request.POST.get('empresa-codigo_reuup'),
                                                nombre=request.POST.get('empresa-nombre'))
            if pj:
                print('instancia de formulario procedencia empresa detectado')
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa',
                                                                instance=pj.first(), empty_permitted=True,
                                                                use_required_attribute=False)
            else:
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa', empty_permitted=True,
                                                                use_required_attribute=False)
        elif request.POST.get('gob-nombre'):
            print('formulario procedencia gobierno detectado')
            gob = Gobierno.objects.filter(nombre=request.POST.get('gob-nombre')[0])
            if gob:
                print('instancia de formulario procedencia gobierno detectado')
                procedence_form = gform = QGobiernoForm(request.POST, prefix='gob', use_required_attribute=False,
                                                        instance=gob.first(), empty_permitted=True)
            else:
                procedence_form = gform = QGobiernoForm(request.POST, prefix='gob', use_required_attribute=False,
                                                        empty_permitted=True)
        elif request.POST.get('organiza-nombre'):
            print('formulario procedencia org detectado')
            org = Organizacion.objects.filter(nombre=request.POST.get('organiza-nombre')[0])
            if org:
                print('instancia de formulario procedencia org detectado')
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza', use_required_attribute=False,
                                                            instance=org.first(), empty_permitted=True)
            else:
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza', use_required_attribute=False,
                                                            empty_permitted=True)

        if request.POST.get('personas_list'):
            print('detectado persona por personals list')
            persona_list = request.POST.get('personas_list')
            persona = PersonaNatural.objects.filter(id=persona_list[0]).first()
            print('persona', model_to_dict(persona))
            if persona:
                pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', empty_permitted=True,
                                             use_required_attribute=False, instance=persona)
                print('detectado persona de la lista y agregado al form como instancia')
        else:
            persona = PersonaNatural.objects.filter(ci=request.POST.get('person_queja-ci'),
                                                    nombre__iexact=request.POST.get('person_queja-nombre'),
                                                    apellidos__iexact=request.POST.get('person_queja-apellidos'))
            if persona:
                pnform = QPersonaNaturalForm(request.POST, prefix='person_queja', empty_permitted=True,
                                             use_required_attribute=False, instance=persona)
                print("detctada coincidencia de persona aquejada en la db")

        if form.is_valid() and procedence_form.is_valid() and pnform.is_valid():
            print('formularios validos')
            procedence = procedence_form.save()
            print('salva formulario procedencias')
            if procedence:
                ct = ContentType.objects.get_for_model(procedence)
                proc = Procedencia.objects.create(objecto_contenido=procedence, tipo_contenido=ct, id_objecto=procedence.id)
                proc.save_and_log(request=request, af=0)
            else:
                proc, pcreated = Procedencia.objects.get_or_create(nombre="Anónimo", tipo=TipoProcedencia.objects.filter(id=1).first())

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
            var1 = form.is_valid()
            var2 = pnform.is_valid()
            var3 = pjform.is_valid()
            var4 = tform.is_valid()
            var5 = eform.is_valid()
            var6 = orgform.is_valid()
            var7 = oform.is_valid()
            var8 = gform.is_valid()
            var9 = aqform.is_valid()
    return render(request, 'dpv_quejas/form.html', {'form': form,
                                                    'pnform': pnform,
                                                    'pjform': pjform,
                                                    'tform': tform,
                                                    'eform': eform,
                                                    'orgform': orgform,
                                                    'oform': oform,
                                                    'peform': peform,
                                                    'gform': gform,
                                                    'aqform': aqform})


def editar_queja(request, id_queja):
    return render(request, 'dpv_quejas/form.html')


def eliminar_queja(request, id_queja):
    return render(request, 'dpv_quejas/delete.html')


@permission_required('dpv_quejas.add_asignaquejadpto', raise_exception=True)
def asignar_queja_depto(request, id_queja):
    depto=AsignaQuejaDpto()
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
    tecnico.quejatecnico = Queja.objects.filter(id=id_queja).first()
    form = AsignaQuejaTecnicoForm(instance=tecnico)
    if request.method == 'POST':
        form = AsignaQuejaTecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
            return redirect(reverse_lazy('quejas_list'))
        else:
            return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form})
    else:
        return render(request, 'dpv_quejas/asignar_tecnico.html', {'form': form, 'queja': id_queja})


def responder_queja(request, id_queja):
    return render(request, 'dpv_quejas/responder.html')


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
