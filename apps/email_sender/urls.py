from django.contrib import admin
from django.urls import path
from .views import contactview, emailview


urlpatterns = [
    path('contact', contactview, name="contact"),
    path('email', emailview, name="email"),

]