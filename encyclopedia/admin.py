from django.contrib import admin
from .models import *

# Register your models here.
class NewAdmin(admin.ModelAdmin):
    form = New
admin.site.register(Entry, NewAdmin)