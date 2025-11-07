from django import forms
from .models import ImageRecord


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageRecord
        fields = ['image', 'title', 'description', 'latitude', 'longitude', 'location_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter image title (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter description (optional)',
                'rows': 3
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Latitude (optional)',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Longitude (optional)',
                'step': '0.000001'
            }),
            'location_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Location name (optional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/jpeg,image/png,image/jpg'
            })
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Validate file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 10MB.")
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if image.content_type not in allowed_types:
                raise forms.ValidationError("Only JPEG and PNG images are allowed.")
        
        return image
