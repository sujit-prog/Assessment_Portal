from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
     path('submit-quiz/', views.submit_quiz, name='submit_quiz'), 
      path('subjects/quiz/<int:category_id>/submit/', views.submit_quiz, name='submit_quiz'),
      path('quiz/<int:category_id>/', views.start_quiz, name='start_quiz'),
      path('start-assessment/', views.select_category, name='select_category'),
         path('result/', views.result_page, name='result_page'),
          path('subjects/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
          path('result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
]
