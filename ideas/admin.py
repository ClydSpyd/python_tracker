from django.contrib import admin

from .models import Idea
@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'tags_display', 'created_at')
    def tags_display(self, obj):
        return ", ".join(obj.tags) if obj.tags else ""
    tags_display.short_description = 'Tags'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'tags' in form.base_fields:
            form.base_fields['tags'].widget = admin.widgets.AdminTextInputWidget()
        return form
    
    search_fields = ('title', 'tags', 'user__username')
    list_filter = ('created_at',)
