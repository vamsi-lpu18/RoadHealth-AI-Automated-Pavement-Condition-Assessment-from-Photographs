from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class ImageRecord(models.Model):
    """Model for storing uploaded road images"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Analysis'),
        ('processing', 'Processing'),
        ('analyzed', 'Analyzed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='road_images/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Geolocation fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    
    # Metadata
    upload_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    file_size = models.IntegerField(null=True, blank=True)  # in bytes
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Image Record'
        verbose_name_plural = 'Image Records'
        indexes = [
            models.Index(fields=['-upload_date']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title or 'Image'} - {self.user.email} - {self.upload_date.strftime('%Y-%m-%d')}"
    
    @property
    def has_location(self):
        return self.latitude is not None and self.longitude is not None
    
    def save(self, *args, **kwargs):
        if self.image:
            self.file_size = self.image.size
            # Get image dimensions
            from PIL import Image
            try:
                img = Image.open(self.image)
                self.image_width, self.image_height = img.size
            except:
                pass
        super().save(*args, **kwargs)
