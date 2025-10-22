from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # root landing page
    path('subjects/', include('home.urls')),  # category/subject selection page
]
