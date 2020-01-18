from django.shortcuts import render, redirect
from apps.email_sender.forms import ConfigureMailForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.apps import apps as all_apps
from django.views.defaults import page_not_found, server_error, bad_request, permission_denied
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm, RecoverPassForm
from .forms import GroupForm, UserMForm, UserNPForm, UserPasswordForm, SetPasswordCAForm, PasswordResetCAForm
from .utils import store_url_names
from apps.dpv_persona.models import PersonaNatural
from apps.dpv_persona.forms import PersonaNaturalMForm
from apps.dpv_perfil.models import Perfil
from apps.dpv_perfil.forms import PerfilMForm
from apps.email_sender.models import EmailConfigurate
from apps.dpv_base.mixins import perform_log
from .utils import set_settings_email_conf, comapare_db_settings_conf, get_settings_email_conf

# Create your views here.
@login_required()
def index(request):
    return render(request, 'layouts/dashboard.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('base_dashboard'))
    else:
        store_url_names()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                user_pass = form_data.get('password_login')
                user_name = form_data.get('username_login')
                not_expiry = form_data.get('remenber_me')
                user = User.objects.filter(Q(email=user_name) | Q(username=user_name)).first()
                if user and user.is_active:
                    access = authenticate(username=user.username, password=user_pass)
                    if access:
                        login(request, access)
                        if not_expiry:
                            request.session.set_expiry(4838400)
                        perform_log(request=request, af=3)
                        return redirect(reverse_lazy('base_dashboard'))
                    else:
                        form.add_error('password_login', _('Combinación no válida de usuario y contraseña'))
                else:
                    form.add_error('username_login', _('Ese usuario no exitse o está incativo contacte con el administrador del sistema'))
            else:
                form.add_error('password_login', _('Error de usuario o contraseña no valido'))
            print(form.errors)
            return render(request, 'layouts/login.html', { 'form': form })
        else:
            form = LoginForm()
            return render(request, 'layouts/login.html', { 'form': form })


def recover_pass_page(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('base_dashboard'))
    else:
        if request.method == 'POST':
            pass
        else:
            form = RecoverPassForm
            return render(request, 'layouts/recoverpass/recoverpass.html', {'form': form})

    return render(request, 'layouts/recoverpass/recoverpass.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect(reverse_lazy('base_login'))


@permission_required('auth.view_user', raise_exception=True)
def groups_view(request):
    grupos = Group.objects.all()
    return render(request, 'layouts/admin/groups.html', {'grupos': grupos})


@permission_required('auth.add_user', raise_exception=True)
def user_add(request):
    exist_perfil = False
    exist_persona = False
    if all_apps.get_app_configs():
        for app in all_apps.get_app_configs():
            if 'dpv_perfil' in app.label:
                exist_perfil = True
            if 'dpv_persona' in app.label:
                exist_persona = True
    if request.method == 'POST':
        form = UserMForm(request.POST)
        if exist_persona:
            formprs = PersonaNaturalMForm(request.POST)
        if exist_perfil:
            formprf = PerfilMForm(request.POST)
        if form.is_valid() and formprs.is_valid() and formprf.is_valid():
            usr = form.save()
            usr.set_password(form.cleaned_data.get('password'))
            usr.save()
            try:
                prs = formprs.save()
                prs.nombre = usr.first_name
                prs.apellidos = usr.last_name
                prs.email_address = usr.email
                prs.save()
                try:
                    prf = Perfil()
                    prf.centro_trabajo = formprf.cleaned_data.get('centro_trabajo')
                    prf.depto_trabajo = formprf.cleaned_data.get('depto_trabajo')
                    prf.notificacion_email = formprf.cleaned_data.get('notificacion_email')
                    prf.documentacion_email = formprf.cleaned_data.get('documentacion_email')
                    prf.datos_personales = prs
                    prf.datos_usuario = usr
                    prf.save()
                except:
                    usr.delete()
                    prs.delete()
            except:
                form.add_error('email', 'ya existe algún usuario que está usando ese email')
                return render(request, 'layouts/admin/users_form.html', {'form': form, 'formprs': formprs, 'formprf': formprf })
            perform_log(obj=usr, request=request, af=0)
            return redirect('admin_user')
        else:
            return render(request, 'layouts/admin/users_form.html', {'form': form, 'formprs': formprs, 'formprf': formprf })
    else:
        form = UserMForm()
        if exist_persona:
            formprs = PersonaNaturalMForm()
        if exist_perfil:
            if request.user.perfil_usuario.centro_trabajo.oc:
                formprf = PerfilMForm()
            else:
                prfl = Perfil()
                prfl.centro_trabajo = request.user.perfil_usuario.centro_trabajo
                formprf = PerfilMForm(instance=prfl)

    return render(request, 'layouts/admin/users_form.html', {'form': form, 'formprs': formprs, 'formprf': formprf })


@permission_required('auth.add_group', raise_exception=True)
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            grp = form.save()
            perform_log(obj=grp, request=request, af=0)
            return redirect('admin_group')
        else:
            return render(request, 'layouts/admin/groups_form.html', {'form': form})
    else:
        form = GroupForm()
        return render(request, 'layouts/admin/groups_form.html', {'form': form})


@permission_required('auth.view_user', raise_exception=True)
def users_view(request):
    usuarios = User.objects.none()
    try:
        perfil = request.user.perfil_usuario
        try:
            ct = perfil.centro_trabajo
            if ct.oc:
                usuarios = User.objects.all().exclude(is_superuser=True)
            else:
                usuarios = User.objects.filter(perfil_usuario__centro_trabajo=request.user.perfil_usuario.centro_trabajo).exclude(is_superuser=True)
        except:
            print("no tiene centro de trabajo asociado")
    except:
        print("no tiene perfil asociado")
    return render(request, 'layouts/admin/users.html', {'usuarios': usuarios})


@permission_required('auth.view_logentry', raise_exception=True)
def logs_view(request):
    pass


@permission_required('email_sender.add_emailconfigurate', raise_exception=True)
def configure_email(request):
    ec = EmailConfigurate.objects.all().first()
    sd = get_settings_email_conf()
    equal_data = comapare_db_settings_conf(ec, sd)
    messageok = "Todo concuerda en la configuración de correo guardada en la Base de datos con la información cargada en el settings"
    messageerror = "Existe falta de concordancia entre la cofiguración de correo guarda en la base de datos y la cargada en el settings"
    if equal_data:
        message = messageok
    else:
        message = messageerror
    if request.method == 'POST':
        form = ConfigureMailForm(request.POST, instance=ec)
        if form.is_valid():
            conf = form.save()
            set_settings_email_conf(conf)
            conf.perform_log(request=request, af=0)
            return render(request, 'layouts/admin/mailconf.html', {'form': form, 'ec': ec, 'message': message})
        else:
            return render(request, 'layouts/admin/mailconf.html', {'form': form, 'ec': ec, 'message': message})
    else:
        form = ConfigureMailForm(instance=ec)
        return render(request, 'layouts/admin/mailconf.html', {'form': form, 'ec': ec, 'message': message})


@permission_required('auth.change_user', raise_exception=True)
def user_edit(request, id_usuario):
    usr = User.objects.filter(id=id_usuario).first()
    prf = Perfil.objects.filter(datos_usuario=usr.id).first()
    prs = PersonaNatural.objects.filter(id=prf.datos_personales.id).first()
    if request.method == 'POST':
        form = UserNPForm(request.POST, instance=usr)
        formprs = PersonaNaturalMForm(request.POST, instance=prs)
        formprf = PerfilMForm(request.POST, instance=prf)
        if form.is_valid() and formprf.is_valid() and formprs.is_valid():
            usr = form.save()
            formprs.save()
            formprf.save()
            perform_log(obj=usr, request=request, af=1)
            return redirect(reverse_lazy('admin_user'))
    form = UserNPForm(instance=usr)
    formprs = PersonaNaturalMForm(instance=prs)
    formprf = PerfilMForm(instance=prf)
    return render(request, 'layouts/admin/users_form.html', {'form': form, 'formprs': formprs, 'formprf': formprf})


@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, id_group):
    grp = Group.objects.filter(id=id_group).first()
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grp)
        if form.is_valid():
            grp = form.save()
            perform_log(obj=grp, request=request, af=1)
            return redirect(reverse_lazy('admin_group'))
    else:
        form = GroupForm(instance=grp)
    return render(request, 'layouts/admin/groups_form.html', {'form': form})


@permission_required('auth.delete_user', raise_exception=True)
def user_deactivate(request, id_usr):
    if id_usr != request.user.id:
        usr = User.objects.filter(id=id_usr).first()
        if request.method == 'POST':
            usr.is_active = not usr.is_active
            usr.save()
            perform_log(obj=usr, request=request, af=2)
            return redirect(reverse_lazy('admin_user'))
        return render(request, 'layouts/admin/user_deactivate.html', {'usr': usr})
    return redirect(reverse_lazy('admin_user'))


@permission_required('auth.change_user', raise_exception=True)
def user_setpass(request, id_usr):
    usr = User.objects.filter(id=id_usr).first()
    form = UserPasswordForm(instance=usr)
    if request.method == 'POST':
        form = UserPasswordForm(request.POST, instance=usr)
        if form.is_valid():
            usr.set_password(form.cleaned_data.get('password'))
            usr.save()
            perform_log(obj=usr, request=request, af=1)
            return redirect(reverse_lazy('admin_user'))
    return render(request, 'layouts/admin/user_setpass.html', {'form': form, 'usr': usr})


@permission_required('auth.view_user', raise_exception=True)
def user_detail(request, id_usuario):
    usuario = User.objects.filter(id=id_usuario).first()
    return render(request, 'layouts/admin/user_detail.html', {'usuario': usuario})


@permission_required('auth.view_group', raise_exception=True)
def group_detail(request, id_grp):
    grupo = Group.objects.filter(id=id_grp).first()
    return render(request, 'layouts/admin/groups_view.html', {'grupo': grupo})


@permission_required('auth.view_group', raise_exception=True)
def group_delete(request, id_grp):
    grupo = Group.objects.filter(id=id_grp).first()
    if request.method == 'POST':
        perform_log(obj=grupo, request=request, af=2)
        grupo.delete()
        return redirect(reverse_lazy('admin_group'))
    return render(request, 'layouts/admin/groups_delete.html', {'grupo': grupo})


class RecoverPassBaseView(auth_views.PasswordResetView):
    email_template_name = 'layouts/recoverpass/recoverpass_email.html'
    template_name = 'layouts/recoverpass/recoverpass.html'
    form_class = PasswordResetCAForm


class RecoverPassDoneView(auth_views.PasswordResetDoneView):
    template_name = 'layouts/recoverpass/recoverpass_done.html'


class RecoverPassConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'layouts/recoverpass/recoverpass_confirm.html'
    form_class = SetPasswordCAForm


class RecoverPassCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'layouts/recoverpass/recoverpass_complete.html'


def change_pass(request):
    passform = PasswordChangeForm(request.user)
    if request.method == 'POST':
        passform = PasswordChangeForm(request.user, request.POST)
        if passform.is_valid():
            usr = passform.save()
            update_session_auth_hash(request, usr)
            perform_log(obj=usr, request=request, af=1)
            return redirect(reverse_lazy('perfil_detail'))
    return render(request, 'layouts/admin/change_pass.html', {'passform': passform})


def error400(request):
    return bad_request(request, template_name='400.html')


def error403(request):
    return permission_denied(request, template_name='403.html')


def error404(request):
    return page_not_found(request, template_name='404.html')


def error500(request):
    return server_error(request, template_name='500.html')
