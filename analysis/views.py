# Analysis views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AnalysisResult

@login_required
def analysis_list(request):
    """List all analysis results"""
    results = AnalysisResult.objects.filter(
        image_record__uploaded_by=request.user
    ).order_by('-created_at')
    
    return render(request, 'analysis/analysis_list.html', {
        'results': results
    })
