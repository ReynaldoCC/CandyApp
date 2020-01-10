from django.conf.urls import url
from django.urls import re_path
from . import views as complaint_view
from .index import index as complaint_index
from .render_form import render_forms as rendered_form
from .render_form import render_natural_complaint_form as render_natural_complaint
from .render_form import render_juridic_complaint_form as render_juridic_complaint

urlpatterns = [
    url(r'^$', complaint_view.main_view, name='main_complaint'),
    url(r'^natural/$', complaint_index.index_natural_complaint, name="index_natural_complaint"),
    url(r'^juridic/$', complaint_index.index_juridic_complaint, name="index_juridic_complaint"),
    url(r'^natural/new$', render_natural_complaint.form_person_for_complaint, name="add_natural_person"),
    url(r'^juridic/new$', render_juridic_complaint.form_juridic_for_complaint, name="add_juridic_person"),
    url(r'^wait_distribution/$', complaint_index.index_waiting_for_distribution, name="waiting_for_distribution"),
    url(r'^finished/$', complaint_index.index_finished_complaint, name="index_finished_complaint"),
    url(r'^accepted_all/$', complaint_index.index_accepted, name="index_accepted_all"),
    url(r'^technicals/$', complaint_index.index_technical, name="index_technicals"),
    url(r'^statistics/$', complaint_index.statistics, name="index_technicals"),


    re_path(r'^search/(?P<type_complaint>[0-1])/$', complaint_index.search, name='search'),
    re_path(r'^complaint_nat/(?P<person_id>[1-9]\d*)/$', render_natural_complaint.form_natural_complaint,
            name='add_natural_complaint'),
    re_path(r'^complaint_juridic/(?P<juridic_id>[1-9]\d*)/$', render_juridic_complaint.form_juridic_complaint,
            name='add_juridic_complaint'),
    re_path(r'^complaints_by_person/(?P<person_id>[1-9]\d*)/$', render_natural_complaint.middle_form_natural_complaint,
            name='complaints_by_person'),
    re_path(r'^complaints_by_juridic/(?P<juridic_id>[1-9]\d*)/$',
            render_juridic_complaint.middle_form_juridic_complaint, name='complaints_by_juridic'),
    re_path(r'^get_accepted/(?P<accepted_id>[1-9]\d*)/$', complaint_index.index_accepted_all,
            name='accepted_complaint'),
    re_path(r'^assign_department/(?P<complaint_id>[1-9]\d*)/$', rendered_form.assign_department,
            name='assign_department'),
    re_path(r'^assigned_to_technical/(?P<technical_id>[1-9]\d*)/$',
            complaint_index.index_assigned_to_technician, name="index_assigned_to_technical"),
    re_path(r'^add_finished/(?P<complaint_id>[1-9]\d*)/(?P<technical_id>[0-9]*)/$',
            complaint_view.from_assigned_to_technician_to_finished_complaint, name="form_finished_complaint"),
    re_path(r'^complaint/(?P<complaint_id>[1-9]\d*)/$', complaint_index.watch_complaint, name="watch_complaint"),
    re_path(r'^watch_finished/(?P<finished_id>[1-9]\d*)/$', complaint_index.watch_finished, name="watch_finished"),
    re_path(r'^trans_wait_to_assigned/(?P<complaint_id>[1-9]\d*)/(?P<department_id>[1-9]\d*)/'
            r'(?P<municipality_id>[1-9]\d*)/$',
            complaint_view.from_waiting_for_distribution_to_assigned_to_technician, name='trans_wait_to_assigned'),
    re_path(r'^trans_finished_to_accepted/(?P<complaint_id>[1-9]\d*)/(?P<technical_id>[1-9]\d*)/$',
            complaint_view.from_finished_complaint_to_accepted_complaint, name='trans_Finished_to_Accepted'),
]
