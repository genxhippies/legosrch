from django.conf.urls import patterns, include, url
from django.contrib import admin

import views
import v1.urls

urlpatterns = patterns('',
    # Examples:
    url(r'v1/', include('api.v1.urls', namespace='v1')),
)

