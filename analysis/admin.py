from django.contrib import admin
from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('image_record', 'defect_type', 'condition_label', 'severity_score', 'ai_confidence', 'analyzed_at')
    list_filter = ('defect_type', 'condition_label', 'analyzed_at', 'model_name')
    search_fields = ('image_record__title', 'image_record__user__email', 'defect_type')
    readonly_fields = ('analyzed_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Image Information', {
            'fields': ('image_record',)
        }),
        ('Analysis Results', {
            'fields': ('defect_type', 'severity_score', 'condition_label', 'ai_confidence')
        }),
        ('Model Information', {
            'fields': ('model_name', 'model_version', 'analysis_metadata'),
            'classes': ('collapse',)
        }),
        ('Maintenance', {
            'fields': ('maintenance_suggestion',)
        }),
        ('Images', {
            'fields': ('annotated_image',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('analyzed_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manual addition - should be created by AI analysis
        return False
