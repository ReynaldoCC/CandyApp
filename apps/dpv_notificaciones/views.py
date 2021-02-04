from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import model_to_dict

from .models import Notify
from .forms import NotifyForm

DEFAULT_SHOW_ITEMS = 20


# Create your views here.
# -----------------------------------------------AJAX VIEWS
def my_notifies_json(request):
    """
    View function to get the list of an user notification, this function is maked to use it with datatables of jquery,
    can be used with any ajax call, it waiting the GET variables 'draw', 'strat', 'length', 'search[value]',
    'order[0][column]' and order[0][dir]'. those varaiables are used by datatbles to get ordered, paginated and
    filtrered information, but even not come that variables in request this function response with a full data in a
    JsonResponse.
    :param request: Request object
    :return: [View, JsonResponse] A view rendered or a JsonResponse if request is ajax
    """
    # Get request get method variables from datatable uses
    draw = int(request.GET.get("draw"))
    start = int(request.GET.get("start"))
    length = int(request.GET.get("length")) or DEFAULT_SHOW_ITEMS
    search = request.GET.get("search[value]")
    order_column = request.GET.get("order[0][column]")
    order_direction = request.GET.get("order[0][dir]")

    # Get default query elements
    user = request.user
    user_query = Q(user=user)
    query = Q(id__isnull=False)

    # search and order params from datatables
    if search:
        query = Q(main_text__icontains=search)
    if order_column == "1":
        order_query = "level"
    elif order_column == "2":
        order_query = "readed"
    elif order_column == "3":
        order_query = "id"
    else:
        order_query = "-date_time"
    if order_direction and order_direction == "desc":
        order_query = "-" + order_query

    # Get the notifications
    if start is not None:
        my_notifies = Notify.objects.filter(user_query, query).order_by(order_query)[start:length]
    else:
        my_notifies = Notify.objects.filter(user_query, query).order_by(order_query)

    total = Notify.objects.filter(user_query, query).count()
    response_dict = {
        "sEcho": draw,
        "iTotalRecords": total,
        "iTotalDisplayRecords": total,
        "aaData": my_notifies.values("id", "main_text", "date_time", "level", "readed", )
    }
    return JsonResponse(data=response_dict, status=200)


@login_required()
def toogle_readed_json(request, id_notify):
    notify = get_object_or_404(Notify, id=id_notify)
    if notify.user == request.user:
        notify.readed = not notify.readed
        notify.save()
        message = "La notificación fue marcada como leida satisfactoriamente" \
            if notify.readed else "La notificación fue marcada como no leida satisfactoriamente"
        return JsonResponse(data={"message": message,
                                  "id": notify.id}, status=200)
    return JsonResponse(data={"message": "No se puede modificar una notificación de otro usuario"}, status=403)


@login_required()
def delete_notify_json(request, id_notify):
    """
    View function for remove a notification, this function is used by http method POST and Ajax, this function evaluate
    if the logged user is the owner of the notify
    :param request: Request object
    :param id_notify: Int PK of Notify item to remove
    :return: JsonResponse with message
    """
    notify = get_object_or_404(Notify, id=id_notify)
    if request.method == "POST":
        if notify.user == request.user:
            notify.delete()
            return JsonResponse(data={"message": "Notificación eliminada satisfactoriamente"}, status=204)
        return JsonResponse(data={"message": "No se puede modificar una notificación de otro usuario"}, status=403)
    return JsonResponse(data={"message": "Método HTTP no permitido"}, status=405)


@login_required()
def has_new_notifies(request):
    """
    View function to know if the logged user has any unreaded notification
    :param request: Request object
    :return: JsonResponse with field news indicate the number of unreaded notifies
    """
    how_many = Notify.objects.filter(user=request.user, readed=False).count()
    return JsonResponse(data={"news": how_many}, status=200)


@login_required()
def view_notify_json(request, id_notify):
    """
    View function to get details about notify in jsonresponse, like text, datetime, and level, this fucntion
    automaticaly mark as readed the notify, before that evaluate if the is viewed by the owner to give data
    :param request: Request object
    :param id_notify: Int PK of notify to get details
    :return: JsonResponse
    """
    notify = get_object_or_404(Notify, id=id_notify)
    if notify.user == request.user:
        notify.readed = True
        notify.save()
        notify_dict = model_to_dict(notify)
        return JsonResponse(data=notify_dict, status=200)
    return JsonResponse(data={"message": _("Esta tratando de ver una notificación de otro usuario")}, status=403)


# ---------------------------------------------------HTTP VIEWS
@login_required()
def my_notifies(request):
    """
    View function to show the logged user notifications paginated
    :param request: Request object
    :return: A View
    """
    notify_list = Notify.objects.filter(user=request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(notify_list, DEFAULT_SHOW_ITEMS)
    try:
        notifies = paginator.page(page)
    except PageNotAnInteger:
        notifies = paginator.page(1)
    except EmptyPage:
        notifies = paginator.page(paginator.num_pages)

    return render(request, 'dpv_notificaciones/mylist.html', {'notifies': notifies})


@login_required()
def my_notifies_empty(request):
    """
    View function to show empty page of notifications
    :param request: Request object
    :return: A View
    """
    return render(request, 'dpv_notificaciones/mylist.html', {'notifies': None})


@login_required()
def toogle_readed(request, id_notify):
    """
    View function for toogle the readed field of one notify, this function evaluate if the logged user is the owner of
    the notify
    :param request: Request object
    :param id_notify: Int PK of notify to toggle readed field
    :return: A View
    """
    notify = get_object_or_404(Notify, id=id_notify)
    if request.method == "POST":
        if notify.user == request.user:
            notify.readed = not notify.readed
            notify.save()
            message = _("La notificación fue marcada como leida satisfactoriamente") \
                if notify.readed else _("La notificación fue marcada como no leida satisfactoriamente")
            messages.success(request, message)
            return redirect(reverse_lazy("notifies"))
        messages.warning(request, _("No se puede marcar una notifición de otro usuario"))
        return redirect(reverse_lazy("notifies"))
    return render(request, 'dpv_notificaciones/sure_toggle.html', {"notify": notify})


@login_required()
def delete_notify(request, id_notify):
    """
    View function for remove a notification, this function is used by http method POST, this function evaluate
    if the logged user is the owner of the notify
    :param request: Request object
    :param id_notify: Int PK of Notify item to remove
    :return: JsonResponse with message
    """
    notify = get_object_or_404(Notify, id=id_notify)
    if request.method == "POST":
        if notify.user == request.user:
            notify.delete()
            messages.success(request, _("Notificación eliminada satisfactoriamente"))
            return redirect(reverse_lazy("notifies"))
        messages.warning(request, _("No se puede modificar una notificación de otro usuario"))
        return redirect(reverse_lazy("notifies"))
    return render(request, 'dpv_notificaciones/remove.html', {"notify": notify})


@login_required()
def view_notify(request, id_notify):
    """
    View function to show details about notify, like text, datetime, and level, this fucntion automaticaly mark as
    readed the notify, before that evaluate if the is viewed by the owner to show data
    :param request: Request object
    :param id_notify: Int PK of notify to show details
    :return: A View
    """
    notify = get_object_or_404(Notify, id=id_notify)
    if notify.user == request.user:
        notify.readed = True
        notify.save()
        return render(request, 'dpv_notificaciones/detail.html', {"notify": notify})
    messages.warning(request, _("Esta tratando de ver una notificación de otro usuario"))
    return redirect(reverse_lazy("notifies"))
