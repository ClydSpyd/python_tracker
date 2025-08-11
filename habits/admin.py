from django.contrib import admin

from .models import Habit, HabitRecord

class HabitRecordInline(admin.TabularInline):  
    model = HabitRecord
    extra = 0  # Do not show empty extra rows
    readonly_fields = ['date']

class HabitAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['title', 'description','target', 'user']
    
    # Make 'created_at' and 'updated_at' non-editable in the admin form
    readonly_fields = ['created_at', 'updated_at']
    
    # Add the inline for HabitRecord
    inlines = [HabitRecordInline] 

admin.site.register(Habit, HabitAdmin)