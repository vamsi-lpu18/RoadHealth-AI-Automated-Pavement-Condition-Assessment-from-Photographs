from rest_framework import serializers
from .models import AnalysisResult


class AnalysisResultSerializer(serializers.ModelSerializer):
    image_title = serializers.CharField(source='image_record.title', read_only=True)
    image_url = serializers.ImageField(source='image_record.image', read_only=True)
    
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'image_record', 'image_title', 'image_url',
            'defect_type', 'severity_score', 'condition_label',
            'ai_confidence', 'annotated_image', 'model_name',
            'model_version', 'analysis_metadata', 'maintenance_suggestion',
            'analyzed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'analyzed_at', 'updated_at']
