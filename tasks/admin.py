from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['title', 'status', 'created_at', 'updated_at', 'completed_at']
    
    # Make 'created_at' and 'updated_at' non-editable in the admin form
    readonly_fields = ['created_at', 'updated_at', 'completed_at']

admin.site.register(Task, TaskAdmin)