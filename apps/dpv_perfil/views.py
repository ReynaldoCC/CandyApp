from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PerfilPForm
from apps.dpv_persona.forms import PersonaNaturalProfileForm


# Create your views here.
@login_required()
def index(request):
    profileform = PerfilPForm(instance=request.user.perfil_usuario)
    personform = PersonaNaturalProfileForm(instance=request.user.perfil_usuario.datos_personales)
    if request.method == 'POST':
        profileform = PerfilPForm(request.POST, request.FILES, instance=request.user.perfil_usuario)
        personform = PersonaNaturalProfileForm(request.POST, instance=request.user.perfil_usuario.datos_personales)
        if profileform.is_valid() and personform.is_valid():
            avat = profileform.save()
            model = personform.save()
            avat.perform_log(request=request, af=1)
            model.perform_log(request=request, af=1)
            return render(request, 'dpv_perfil/detail.html', {'profileform': profileform, 'personform': personform})
        return render(request, 'dpv_perfil/detail.html', {'profileform': profileform, 'personform': personform})
    return render(request, 'dpv_perfil/detail.html', {'profileform': profileform, 'personform': personform})
