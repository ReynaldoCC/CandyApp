from django.urls import path
from .views import my_notifies, my_notifies_json, delete_notify, delete_notify_json, toogle_readed, \
    toogle_readed_json, my_notifies_empty, has_new_notifies, view_notify, view_notify_json

urlpatterns = [
    path('', my_notifies, name='notifies'),
    path('json/', my_notifies_json, name='notifies_json'),
    path('empty/', my_notifies_empty, name='notifies_empty'),
    path('<int:id_notify>', view_notify, name='notifies_detail'),
    path('<int:id_notify>/json', view_notify_json, name='notifies_detail_json'),
    path('delete/<int:id_notify>', delete_notify, name='notifies_del'),
    path('delete/json/<int:id_notify>', delete_notify_json, name='notififes_del_json'),
    path('toggle/<int:id_notify>', toogle_readed, name='notififes_togg'),
    path('toggle/json/<int:id_notify>', toogle_readed_json, name='notifies_togg_json'),
    path('news', has_new_notifies, name='notifies_news'),

]