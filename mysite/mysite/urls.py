from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('quixx/', include('quixx.urls')),
    path('admin/', admin.site.urls),
]
