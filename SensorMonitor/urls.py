from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import os
from SensorMonitor import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'SensorMonitorPanel.views.home'),
    url(r'^sensor/', 'SensorMonitorPanel.views.sensor'),
    url(r'^admin/', include(admin.site.urls)),
) + \
static(r'/js/', document_root=os.path.join(settings.STATIC_ROOT, 'js')) + \
static(r'/images/', document_root=os.path.join(settings.STATIC_ROOT, 'images'))
