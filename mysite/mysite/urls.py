from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('qwixx/', include('qwixx.urls')),
    path('admin/', admin.site.urls),
]
