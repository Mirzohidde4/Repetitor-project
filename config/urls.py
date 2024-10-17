from django.contrib import admin
from django.urls import path, include
from main.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage, name='home'),
    path('api/', include('api.urls')),
]
