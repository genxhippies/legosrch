from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = [
    # Examples:
    url(r'item_number/(?P<num>[0-9A-Za-z]+)/', views.item_number),
]
