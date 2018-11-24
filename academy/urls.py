from django.contrib import admin
from django.urls import path, include
from academy.views import _class, _section, _session, api_attendance, api_section_last_session, api_section_create

app_name = "attendance"
urlpatterns = [
    path('', _class,name='classes'),
    path('<course>/<section>/', _section,name='sections'),
    path('<course>/<section>/<session>', _session,name='section'),
    path('api/<course>/<section>/<session>/<student_id>/<status>', api_attendance),
    path('api/<course>/<section>/query_last_session', api_section_last_session),
    path('api/<course>/<section>/create', api_section_create),
]
