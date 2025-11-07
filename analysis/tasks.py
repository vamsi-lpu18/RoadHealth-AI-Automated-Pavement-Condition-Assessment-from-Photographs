"""
Celery tasks for asynchronous image analysis
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@shared_task
def analyze_image_task(image_record_id):
    """
    Asynchronous task to analyze an uploaded image.
    
    Args:
        image_record_id: ID of the ImageRecord to analyze
    """
    from core.models import ImageRecord
    from .models import AnalysisResult
    from .ai_model import get_detector
    
    try:
        # Get image record
        image_record = ImageRecord.objects.get(id=image_record_id)
        
        # Update status to processing
        image_record.status = 'processing'
        image_record.save()
        
        logger.info(f"Starting analysis for image {image_record_id}")
        
        # Get AI detector
        detector = get_detector()
        
        # Analyze image
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
        
        # Save annotated image if available
        if results.get('annotated_image_path'):
            from django.core.files import File
            with open(results['annotated_image_path'], 'rb') as f:
                analysis.annotated_image.save(
                    Path(results['annotated_image_path']).name,
                    File(f),
                    save=True
                )
        
        logger.info(f"Analysis complete for image {image_record_id}: {results['defect_type']} - {results['condition_label']}")
        
        # Send email notification for critical conditions
        if results['condition_label'] == 'critical':
            send_critical_alert.delay(image_record_id)
        
        return {
            'status': 'success',
            'image_id': image_record_id,
            'results': results
        }
    
    except ImageRecord.DoesNotExist:
        logger.error(f"ImageRecord {image_record_id} not found")
        return {'status': 'error', 'message': 'Image not found'}
    
    except Exception as e:
        logger.error(f"Error analyzing image {image_record_id}: {str(e)}")
        
        # Update status to failed
        try:
            image_record = ImageRecord.objects.get(id=image_record_id)
            image_record.status = 'failed'
            image_record.save()
        except:
            pass
        
        return {'status': 'error', 'message': str(e)}


@shared_task
def send_critical_alert(image_record_id):
    """
    Send email alert for critical road conditions.
    
    Args:
        image_record_id: ID of the ImageRecord with critical condition
    """
    from core.models import ImageRecord
    
    try:
        image_record = ImageRecord.objects.get(id=image_record_id)
        analysis = image_record.analysis
        
        # Prepare email
        subject = f'CRITICAL: Road Condition Alert - {image_record.location_name or "Unknown Location"}'
        
        message = f"""
CRITICAL ROAD CONDITION DETECTED

Location: {image_record.location_name or 'Not specified'}
Coordinates: {image_record.latitude}, {image_record.longitude}
Uploaded by: {image_record.user.get_full_name() or image_record.user.email}
Upload Date: {image_record.upload_date.strftime('%Y-%m-%d %H:%M')}

ANALYSIS RESULTS:
-----------------
Defect Type: {analysis.get_defect_type_display()}
Severity Score: {analysis.severity_score:.2f}/100
Condition: {analysis.get_condition_label_display()}
AI Confidence: {analysis.ai_confidence * 100:.1f}%

RECOMMENDATION:
{analysis.maintenance_suggestion}

Please review and take immediate action.

---
RoadHealth AI System
        """
        
        # Send to user and admins
        from accounts.models import User
        
        recipients = [image_record.user.email]
        
        # Add admin emails
        admin_emails = User.objects.filter(role='admin').values_list('email', flat=True)
        recipients.extend(admin_emails)
        
        if settings.EMAIL_HOST_USER:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False,
            )
            logger.info(f"Critical alert sent for image {image_record_id}")
        else:
            logger.warning("Email not configured. Alert not sent.")
    
    except Exception as e:
        logger.error(f"Error sending critical alert for image {image_record_id}: {str(e)}")
