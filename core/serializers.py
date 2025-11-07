from rest_framework import serializers
from .models import ImageRecord


class ImageRecordSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    has_analysis = serializers.SerializerMethodField()
    
    class Meta:
        model = ImageRecord
        fields = [
            'id', 'user', 'user_email', 'user_name', 'image', 'title', 
            'description', 'status', 'latitude', 'longitude', 'location_name',
            'upload_date', 'updated_date', 'file_size', 'image_width', 
            'image_height', 'has_location', 'has_analysis'
        ]
        read_only_fields = ['id', 'user', 'upload_date', 'updated_date', 'file_size', 'image_width', 'image_height']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    def get_has_analysis(self, obj):
        return hasattr(obj, 'analysis') and obj.analysis is not None


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRecord
        fields = ['image', 'title', 'description', 'latitude', 'longitude', 'location_name']
    
    def validate_image(self, value):
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Image file size should not exceed 10MB.")
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG and PNG images are allowed.")
        
        return value
    
    def create(self, validated_data):
        # Set user from context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
