
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

urlpatterns = [
    url(r'^admindjango/', include(admin.site.urls)),
    url(r'', include('sistema.urls')),
]

handler404 = 'sistema.views.error_404'