from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from .models import ImageRecord
from .serializers import ImageRecordSerializer, ImageUploadSerializer
from analysis.models import AnalysisResult


class ImageRecordViewSet(viewsets.ModelViewSet):
    """API ViewSet for ImageRecord"""
    serializer_class = ImageRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ImageRecord.objects.all().select_related('user').prefetch_related('analysis')
        return ImageRecord.objects.filter(user=user).prefetch_related('analysis')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ImageUploadSerializer
        return ImageRecordSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dashboard statistics"""
        user = request.user
        queryset = self.get_queryset()
        
        total_images = queryset.count()
        analyzed_images = queryset.filter(status='analyzed').count()
        pending_images = queryset.filter(status='pending').count()
        
        # Defect statistics
        defect_stats = AnalysisResult.objects.filter(
            image_record__in=queryset
        ).values('defect_type').annotate(count=Count('id'))
        
        # Severity distribution
        severity_stats = AnalysisResult.objects.filter(
            image_record__in=queryset
        ).values('condition_label').annotate(count=Count('id'))
        
        # Average severity
        avg_severity = AnalysisResult.objects.filter(
            image_record__in=queryset
        ).aggregate(avg=Avg('severity_score'))['avg'] or 0
        
        return Response({
            'total_images': total_images,
            'analyzed_images': analyzed_images,
            'pending_images': pending_images,
            'defect_stats': list(defect_stats),
            'severity_stats': list(severity_stats),
            'avg_severity': round(avg_severity, 2),
        })
    
    @action(detail=True, methods=['post'])
    def reanalyze(self, request, pk=None):
        """Trigger re-analysis of an image"""
        image = self.get_object()
        
        # Trigger analysis task
        from analysis.tasks import analyze_image_task
        analyze_image_task.delay(image.id)
        
        return Response({
            'message': 'Image queued for re-analysis',
            'status': 'processing'
        })
