from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import AnalysisResult
from .serializers import AnalysisResultSerializer
from core.models import ImageRecord


class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for AnalysisResult (read-only)"""
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return AnalysisResult.objects.all().select_related('image_record__user')
        return AnalysisResult.objects.filter(
            image_record__user=user
        ).select_related('image_record')
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get all critical condition results"""
        queryset = self.get_queryset().filter(condition_label='critical')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_defect_type(self, request):
        """Get results grouped by defect type"""
        defect_type = request.query_params.get('type')
        
        if not defect_type:
            return Response(
                {'error': 'Please provide defect type parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(defect_type=defect_type)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
