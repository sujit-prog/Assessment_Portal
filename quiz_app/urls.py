from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # root goes to landing page
    path('subjects/', include('home.urls')),  # subjects page
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('subjects/', include('home.urls')),
]
