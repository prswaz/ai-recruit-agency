from django.contrib import admin
from .models import AIAgent, AILog


@admin.register(AIAgent)
class AIAgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'function', 'created_at')
    search_fields = ('name', 'function')


@admin.register(AILog)
class AILogAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'agent', 'execution_time_ms', 'created_at')
    search_fields = ('action_type', 'agent__name')
    readonly_fields = ('created_at',)
