from django.contrib import admin
from .models import ImageRecord


@admin.register(ImageRecord)
class ImageRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'upload_date', 'has_location', 'file_size_display')
    list_filter = ('status', 'upload_date', 'user')
    search_fields = ('title', 'description', 'user__email', 'location_name')
    readonly_fields = ('upload_date', 'updated_date', 'file_size', 'image_width', 'image_height')
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description', 'image', 'status')
        }),
        ('Location Data', {
            'fields': ('latitude', 'longitude', 'location_name'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('upload_date', 'updated_date', 'file_size', 'image_width', 'image_height'),
            'classes': ('collapse',)
        }),
    )
    
    def has_location(self, obj):
        return obj.has_location
    has_location.boolean = True
    has_location.short_description = 'Has GPS'
    
    def file_size_display(self, obj):
        if obj.file_size:
            size_mb = obj.file_size / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        return "N/A"
    file_size_display.short_description = 'File Size'
