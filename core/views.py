from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.db.models import Count, Q, Avg
from .models import ImageRecord
from .forms import ImageUploadForm
from analysis.models import AnalysisResult


class HomeView(TemplateView):
    """Home page view"""
    template_name = 'core/home.html'


@login_required
def dashboard_view(request):
    """Main dashboard view with analytics"""
    user = request.user
    
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    if user.is_admin:
        images = ImageRecord.objects.all()
    else:
        images = ImageRecord.objects.filter(user=user)
    
    # Apply filters
    if status_filter:
        images = images.filter(status=status_filter)
    
    if search_query:
        images = images.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )
    
    # Get statistics
    total_images = images.count()
    analyzed_images = images.filter(status='analyzed').count()
    pending_images = images.filter(status='pending').count()
    processing_images = images.filter(status='processing').count()
    
    # Get defect statistics
    defect_stats = AnalysisResult.objects.filter(
        image_record__in=images
    ).values('defect_type').annotate(count=Count('id'))
    
    # Get severity distribution
    severity_stats = AnalysisResult.objects.filter(
        image_record__in=images
    ).values('condition_label').annotate(count=Count('id'))
    
    # Average severity score
    avg_severity = AnalysisResult.objects.filter(
        image_record__in=images
    ).aggregate(avg=Avg('severity_score'))['avg'] or 0
    
    # Recent images
    recent_images = images.select_related('user').prefetch_related('analysis')[:10]
    
    context = {
        'total_images': total_images,
        'analyzed_images': analyzed_images,
        'pending_images': pending_images,
        'processing_images': processing_images,
        'defect_stats': list(defect_stats),
        'severity_stats': list(severity_stats),
        'avg_severity': round(avg_severity, 2),
        'recent_images': recent_images,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def upload_image(request):
    """Image upload view"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_record = form.save(commit=False)
            image_record.user = request.user
            image_record.save()
            
            # Run AI analysis synchronously (without Celery)
            try:
                from analysis.models import AnalysisResult
                from analysis.ai_model import get_detector
                from pathlib import Path
                
                # Update status to processing
                image_record.status = 'processing'
                image_record.save()
                
                # Get AI detector and analyze
                detector = get_detector()
                image_path = image_record.image.path
                results = detector.analyze_image(image_path)
                
                # Save analysis results
                analysis = AnalysisResult.objects.create(
                    image_record=image_record,
                    defect_type=results['defect_type'],
                    severity_score=results['severity_score'],
                    condition_label=results['condition_label'],
                    ai_confidence=results['ai_confidence'],
                    model_name=results['model_name'],
                    model_version=results['model_version'],
                    analysis_metadata=results.get('analysis_metadata', {}),
                )
                
                # Update status to completed
                image_record.status = 'completed'
                image_record.save()
                
                messages.success(request, 'Image uploaded and analyzed successfully!')
            except Exception as e:
                image_record.status = 'failed'
                image_record.save()
                messages.error(request, f'Error analyzing image: {str(e)}')
            
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ImageUploadForm()
    
    return render(request, 'core/upload.html', {'form': form})


@login_required
def image_list(request):
    """List all images"""
    user = request.user
    
    if user.is_admin:
        images = ImageRecord.objects.all().select_related('user').prefetch_related('analysis')
    else:
        images = ImageRecord.objects.filter(user=user).prefetch_related('analysis')
    
    # Filters
    status = request.GET.get('status')
    if status:
        images = images.filter(status=status)
    
    context = {
        'images': images,
        'status_choices': ImageRecord.STATUS_CHOICES,
    }
    
    return render(request, 'core/image_list.html', context)


@login_required
def image_detail(request, pk):
    """View individual image details"""
    image = get_object_or_404(ImageRecord, pk=pk)
    
    # Check permissions
    if not request.user.is_admin and image.user != request.user:
        messages.error(request, 'You do not have permission to view this image.')
        return redirect('dashboard')
    
    # Get analysis result if exists
    analysis = None
    if hasattr(image, 'analysis'):
        analysis = image.analysis
    
    context = {
        'image': image,
        'analysis': analysis,
    }
    
    return render(request, 'core/image_detail.html', context)


@login_required
def map_view(request):
    """Map view showing all geotagged images"""
    user = request.user
    
    if user.is_admin:
        images = ImageRecord.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).select_related('user').prefetch_related('analysis')
    else:
        images = ImageRecord.objects.filter(
            user=user,
            latitude__isnull=False,
            longitude__isnull=False
        ).prefetch_related('analysis')
    
    # Prepare data for map markers
    map_data = []
    for img in images:
        marker = {
            'id': img.id,
            'lat': float(img.latitude),
            'lng': float(img.longitude),
            'title': img.title or 'Road Image',
            'status': img.status,
            'location': img.location_name,
        }
        
        # Add severity info if analyzed
        if hasattr(img, 'analysis') and img.analysis:
            marker['severity'] = img.analysis.condition_label
            marker['defect_type'] = img.analysis.defect_type
        
        map_data.append(marker)
    
    context = {
        'map_data': map_data,
        'google_maps_api_key': '',  # Will be loaded from settings in template
    }
    
    return render(request, 'core/map.html', context)
