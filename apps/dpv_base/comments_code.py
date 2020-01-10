# def user_add(request):
#     exist_perfil = False
#     exist_persona = False
#     if all_apps.get_app_configs():
#         for app in all_apps.get_app_configs():
#             if 'dpv_perfil' in app.label:
#                 exist_perfil = True
#             if 'dpv_persona' in app.label:
#                 exist_persona = True
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if exist_perfil:
#             form = UserProfileForm(request.POST)
#         if exist_persona and exist_perfil:
#             form = FullUserForm(request.POST)
#         if form.is_valid():
#             user = User()
#             user.username = form.cleaned_data.get('username')
#             user.last_name = form.cleaned_data.get('last_name')
#             user.first_name = form.cleaned_data.get('first_name')
#             user.email = form.cleaned_data.get('email')
#             user.set_password(form.cleaned_data.get('password'))
#             user.is_staff = form.cleaned_data.get('is_staff')
#             user.is_active = True
#             user.save()
#             user.user_permissions.set(form.cleaned_data.get('permissions'))
#             user.groups.set(form.cleaned_data.get('groups'))
#             if exist_persona:
#                 persona = PersonaNatural()
#                 persona.ci = form.cleaned_data.get('ci')
#                 persona.genero = form.cleaned_data.get('sexo')
#                 persona.movil = form.cleaned_data.get('movil')
#                 persona.telefono = form.cleaned_data.get('telefono')
#                 persona.direccion_calle = form.cleaned_data.get('direccion_calle')
#                 persona.direccion_numero = form.cleaned_data.get('direccion_numero')
#                 persona.direccion_entrecalle1 = form.cleaned_data.get('direccion_entrecalle1')
#                 persona.direccion_entrecalle2 = form.cleaned_data.get('direccion_entrecalle2')
#                 persona.direccion_municipio = form.cleaned_data.get('direccion_municipio')
#                 persona.nombre = user.first_name
#                 persona.apellidos = user.last_name
#                 persona.email_address = user.email
#                 persona.save()
#             if exist_perfil:
#                 perfil = Perfil()
#                 perfil.notifyemail = form.cleaned_data.get('notificaciones_email')
#                 perfil.docemail = form.cleaned_data.get('documentacion_email')
#                 perfil.depto = form.cleaned_data.get('area_trabajo')
#                 perfil.unidad = form.cleaned_data.get('centro_trabajo')
#                 perfil.datos_usuario = user
#                 perfil.datos_personales = persona
#                 perfil.save()
#             return redirect('admin_user')
#         else:
#             return render(request, 'layouts/admin/users_form.html', {'form': form})
#     else:
#         form = UserForm()
#         if exist_perfil:
#             form = UserProfileForm()
#         if exist_persona and exist_perfil:
#             form = FullUserForm()
#     return render(request, 'layouts/admin/users_form.html', {'form': form})