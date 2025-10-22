from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_selection, name='subject_selection'),
    path('quiz/<int:category_id>/', views.quiz_view, name='quiz_view'),
]
