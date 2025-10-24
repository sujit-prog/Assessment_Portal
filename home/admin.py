from django.contrib import admin
from .models import Category, Question

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')   # Show ID and name in admin list view
    search_fields = ('name',)       # Allow searching by name

# Register Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'question_text', 'correct_option')
    list_filter = ('category', 'correct_option')  # Filter options in sidebar
    search_fields = ('question_text',)            # Search questions
    raw_id_fields = ('category',)                # Use ID lookup for category
