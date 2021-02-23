from django.contrib import admin
from myapp.models import Tool

class ToolAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tool, ToolAdmin)