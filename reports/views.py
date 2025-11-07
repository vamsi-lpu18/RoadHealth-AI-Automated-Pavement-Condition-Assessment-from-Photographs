from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from datetime import datetime
from core.models import ImageRecord
from analysis.models import AnalysisResult
from .pdf_generator import PDFReportGenerator
from .csv_exporter import export_analysis_to_csv


@login_required
def generate_report(request, pk):
    """Generate PDF report for a single image analysis"""
    image_record = get_object_or_404(ImageRecord, pk=pk)
    
    # Check permissions
    if not request.user.is_admin and image_record.user != request.user:
        return HttpResponse("Unauthorized", status=403)
    
    # Check if analysis exists
    if not hasattr(image_record, 'analysis'):
        return HttpResponse("Analysis not found for this image", status=404)
    
    analysis = image_record.analysis
    
    # Generate PDF
    generator = PDFReportGenerator()
    pdf = generator.generate_report(image_record, analysis)
    
    # Create response
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"road_analysis_{image_record.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def export_csv(request):
    """Export analysis data to CSV"""
    user = request.user
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    condition_filter = request.GET.get('condition', '')
    
    # Base queryset
    if user.is_admin:
        analysis_results = AnalysisResult.objects.all().select_related('image_record__user')
    else:
        analysis_results = AnalysisResult.objects.filter(
            image_record__user=user
        ).select_related('image_record')
    
    # Apply filters
    if condition_filter:
        analysis_results = analysis_results.filter(condition_label=condition_filter)
    
    # Generate CSV
    csv_data = export_analysis_to_csv(analysis_results)
    
    # Create response
    response = HttpResponse(csv_data, content_type='text/csv')
    filename = f"road_analysis_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def summary_report(request):
    """Generate summary PDF report for all analyses"""
    user = request.user
    
    # Get data
    if user.is_admin:
        image_records = ImageRecord.objects.all().select_related('user')
        analysis_results = AnalysisResult.objects.all().select_related('image_record__user')
    else:
        image_records = ImageRecord.objects.filter(user=user)
        analysis_results = AnalysisResult.objects.filter(
            image_record__user=user
        ).select_related('image_record')
    
    # Generate PDF
    generator = PDFReportGenerator()
    pdf = generator.generate_summary_report(image_records, analysis_results)
    
    # Create response
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"road_analysis_summary_{datetime.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def report_preview(request, pk):
    """Preview report in browser"""
    image_record = get_object_or_404(ImageRecord, pk=pk)
    
    # Check permissions
    if not request.user.is_admin and image_record.user != request.user:
        return HttpResponse("Unauthorized", status=403)
    
    # Check if analysis exists
    if not hasattr(image_record, 'analysis'):
        return HttpResponse("Analysis not found for this image", status=404)
    
    analysis = image_record.analysis
    
    context = {
        'image': image_record,
        'analysis': analysis,
    }
    
    return render(request, 'reports/report_preview.html', context)
