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
          path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add-question/<int:category_id>/', views.add_question, name='add_question'),
      path('results/', views.view_all_results, name='view_all_results'),
    path('results/export/', views.export_results_csv, name='export_results_csv'),
    path('results/delete/<int:attempt_id>/', views.delete_result, name='delete_result'),
    path('results/user/<int:user_id>/', views.view_user_detail, name='view_user_detail'),
    

]

