from unicodedata import category

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)

class answeradmin(admin.TabularInline):
    model = Answer
    extra = 1


class questionadmin(    admin.ModelAdmin):
    inlines = [answeradmin]
  

admin.site.register(Question, questionadmin)
admin.site.register(Answer)