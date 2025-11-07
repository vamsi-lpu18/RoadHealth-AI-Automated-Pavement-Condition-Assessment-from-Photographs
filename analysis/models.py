from django.db import models
from core.models import ImageRecord


class AnalysisResult(models.Model):
    """Model for storing AI analysis results"""
    
    DEFECT_TYPE_CHOICES = [
        ('crack', 'Crack'),
        ('pothole', 'Pothole'),
        ('rough_surface', 'Rough Surface'),
        ('alligator_crack', 'Alligator Crack'),
        ('edge_crack', 'Edge Crack'),
        ('joint_crack', 'Joint Crack'),
        ('no_defect', 'No Defect'),
    ]
    
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('moderate', 'Moderate'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    
    image_record = models.OneToOneField(
        ImageRecord,
        on_delete=models.CASCADE,
        related_name='analysis'
    )
    defect_type = models.CharField(max_length=50, choices=DEFECT_TYPE_CHOICES)
    severity_score = models.FloatField(help_text="Severity score from 0 to 100")
    condition_label = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    ai_confidence = models.FloatField(help_text="AI model confidence score (0-1)")
    
    # Optional: Store annotated image with bounding boxes
    annotated_image = models.ImageField(upload_to='annotated_images/%Y/%m/%d/', blank=True, null=True)
    
    # AI model information
    model_name = models.CharField(max_length=100, default='DefaultModel')
    model_version = models.CharField(max_length=50, default='1.0')
    
    # Additional analysis data (JSON format)
    analysis_metadata = models.JSONField(default=dict, blank=True)
    
    # Maintenance suggestion
    maintenance_suggestion = models.TextField(blank=True)
    
    # Timestamps
    analyzed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-analyzed_at']
        verbose_name = 'Analysis Result'
        verbose_name_plural = 'Analysis Results'
    
    def __str__(self):
        return f"Analysis: {self.defect_type} - {self.condition_label} ({self.image_record.id})"
    
    def save(self, *args, **kwargs):
        # Auto-generate maintenance suggestion if not provided
        if not self.maintenance_suggestion:
            self.maintenance_suggestion = self.generate_suggestion()
        
        # Update image record status
        if self.image_record.status != 'analyzed':
            self.image_record.status = 'analyzed'
            self.image_record.save()
        
        super().save(*args, **kwargs)
    
    def generate_suggestion(self):
        """Generate maintenance suggestion based on defect type and severity"""
        suggestions = {
            'crack': {
                'good': 'Monitor regularly. Minor crack sealing recommended.',
                'moderate': 'Apply crack sealing treatment within 3 months.',
                'poor': 'Immediate crack repair required. Consider surface overlay.',
                'critical': 'Urgent repair needed. Full depth patching recommended.',
            },
            'pothole': {
                'good': 'Fill small potholes with cold-mix asphalt.',
                'moderate': 'Clean and fill potholes using hot-mix asphalt.',
                'poor': 'Extensive pothole repair required. Consider area patching.',
                'critical': 'Emergency repair needed. Road closure may be necessary.',
            },
            'rough_surface': {
                'good': 'Schedule routine maintenance and surface leveling.',
                'moderate': 'Surface milling and overlay recommended.',
                'poor': 'Major resurfacing required within 6 months.',
                'critical': 'Complete road reconstruction needed.',
            },
            'alligator_crack': {
                'good': 'Monitor and seal cracks to prevent water infiltration.',
                'moderate': 'Remove and replace affected pavement section.',
                'poor': 'Full depth reconstruction required.',
                'critical': 'Immediate structural repair needed. Subbase may be compromised.',
            },
            'edge_crack': {
                'good': 'Seal cracks and improve edge drainage.',
                'moderate': 'Edge repair with shoulder reconstruction.',
                'poor': 'Edge wedge joint repair and shoulder stabilization.',
                'critical': 'Complete edge reconstruction with drainage improvement.',
            },
            'joint_crack': {
                'good': 'Seal joints to prevent water intrusion.',
                'moderate': 'Clean and reseal joints with appropriate materials.',
                'poor': 'Joint replacement and repair required.',
                'critical': 'Urgent joint repair with load transfer restoration.',
            },
            'no_defect': {
                'good': 'Road in excellent condition. Continue regular inspections.',
                'moderate': 'No immediate action required.',
                'poor': 'No immediate action required.',
                'critical': 'No immediate action required.',
            },
        }
        
        return suggestions.get(self.defect_type, {}).get(
            self.condition_label,
            'Consult with a road engineer for proper assessment.'
        )
