from django.db import models

class AIAgent(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)  # مثل 'matcher' یا 'parser'
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version or 'N/A'}"

    class Meta:
        verbose_name = "AI Agent"
        verbose_name_plural = "AI Agents"


class AILog(models.Model):
    agent = models.ForeignKey(AIAgent, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    action_type = models.CharField(max_length=100)  # مثل 'ResumeAnalysis'
    input_data = models.JSONField(blank=True, null=True)
    output_data = models.JSONField(blank=True, null=True)
    execution_time_ms = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"