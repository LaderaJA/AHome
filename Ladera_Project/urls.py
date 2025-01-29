
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AHome_app.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('dashboard/', include('Admin_Dashboard.urls')),
]
