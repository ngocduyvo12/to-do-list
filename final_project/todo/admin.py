from django.contrib import admin
from .models import User, Tasks
# Register your models here.
class MyModelAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp"]

admin.site.register(User)
admin.site.register(Tasks, MyModelAdmin)