from django.contrib import admin
from .models import Space

class SpaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']   


admin.site.register(Space, SpaceAdmin)