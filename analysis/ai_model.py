"""
AI Model for Road Defect Detection

This module contains the AI model integration for analyzing road images.
It uses OpenCV and TensorFlow for image processing and defect detection.
"""

import cv2
import numpy as np
from pathlib import Path
from django.conf import settings
import logging

try:
    import google.generativeai as genai
    _HAS_GEMINI = True
except ImportError:
    genai = None
    _HAS_GEMINI = False

logger = logging.getLogger(__name__)


class RoadDefectDetector:
    """
    AI Model for detecting road defects in images.
    
    This is a placeholder implementation that uses simple image processing.
    In production, replace this with a trained deep learning model.
    """
    
    def __init__(self):
        self.model_name = "SimpleDetector"
        self.model_version = "1.0"
        self.confidence_threshold = getattr(settings, 'AI_CONFIDENCE_THRESHOLD', 0.5)
    
    def load_model(self):
        """
        Load the AI model.
        
        In production, this should load a pre-trained model:
        - TensorFlow/Keras model (.h5)
        - PyTorch model (.pth)
        - ONNX model (.onnx)
        
        Example:
            self.model = tf.keras.models.load_model('path/to/model.h5')
        """
        # Placeholder - implement actual model loading
        logger.info(f"Loading model: {self.model_name} v{self.model_version}")
        pass
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model input.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image array
        """
        # Read image
        img = cv2.imread(str(image_path))
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size (example: 224x224)
        img_resized = cv2.resize(img_rgb, (224, 224))
        
        # Normalize
        img_normalized = img_resized.astype(np.float32) / 255.0
        
        return img, img_normalized
    
    def detect_defects(self, image_array):
        """
        Detect defects in the image.
        
        This is a placeholder implementation using simple image processing.
        Replace with actual model inference in production.
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            Dictionary with detection results
        """
        # Placeholder logic - simulate defect detection
        # In production, use: predictions = self.model.predict(image_array)
        
        # Simple edge detection as placeholder
        gray = cv2.cvtColor((image_array * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Simulate defect classification based on edge density
        if edge_density > 0.15:
            defect_type = 'crack'
            severity = min(edge_density * 300, 100)
        elif edge_density > 0.10:
            defect_type = 'rough_surface'
            severity = min(edge_density * 250, 100)
        elif edge_density > 0.05:
            defect_type = 'edge_crack'
            severity = min(edge_density * 200, 100)
        else:
            defect_type = 'no_defect'
            severity = edge_density * 100
        
        # Simulate confidence score
        confidence = np.random.uniform(0.7, 0.95)
        
        return {
            'defect_type': defect_type,
            'severity_score': float(severity),
            'confidence': float(confidence),
            'metadata': {
                'edge_density': float(edge_density),
                'processing_method': 'canny_edge_detection'
            }
        }
    
    def determine_condition(self, severity_score):
        """
        Determine condition label based on severity score.
        
        Args:
            severity_score: Severity score (0-100)
            
        Returns:
            Condition label string
        """
        if severity_score < 25:
            return 'good'
        elif severity_score < 50:
            return 'moderate'
        elif severity_score < 75:
            return 'poor'
        else:
            return 'critical'
    
    def create_annotated_image(self, original_image, detections):
        """
        Create annotated image with bounding boxes and labels.
        
        Args:
            original_image: Original image array
            detections: Detection results
            
        Returns:
            Annotated image array
        """
        # Create a copy
        annotated = original_image.copy()
        
        # Add text overlay
        defect_type = detections['defect_type']
        severity = detections['severity_score']
        confidence = detections['confidence']
        
        text = f"{defect_type.upper()}: {severity:.1f}% (Conf: {confidence:.2f})"
        
        # Add text to image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            annotated,
            text,
            (10, 30),
            font,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )
        
        # In production, add bounding boxes around detected defects
        # Example: cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        return annotated
    
    def analyze_image(self, image_path):
        """
        Main method to analyze an image.

        If a Gemini API key and library are available, use Gemini Vision to
        classify the road condition. Otherwise, fall back to the simple
        OpenCV-based placeholder model.
        """
        try:
            gemini_key = getattr(settings, "GEMINI_API_KEY", "")

            # Use Gemini if configured, otherwise fallback
            if _HAS_GEMINI and gemini_key:
                logger.info("Using Gemini Vision for road defect analysis")
                genai.configure(api_key=gemini_key)

                model = genai.GenerativeModel("gemini-1.5-flash")

                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                prompt = """
You are a pavement engineer. Analyze this road surface image and respond ONLY with a compact JSON object.
Keys:
- defect_type: one of [crack, pothole, rough_surface, alligator_crack, edge_crack, joint_crack, no_defect]
- severity_score: number from 0 to 100 (higher = worse)
- condition_label: one of [good, moderate, poor, critical]
- ai_confidence: number between 0 and 1
- maintenance_suggestion: 1–3 sentence maintenance recommendation
                """

                response = model.generate_content(
                    [
                        prompt,
                        {
                            "mime_type": "image/jpeg",
                            "data": image_bytes,
                        },
                    ]
                )

                import json

                try:
                    data = json.loads(response.text.strip())
                except Exception:
                    logger.warning("Gemini response not valid JSON, falling back to simple detector")
                    data = None

                if data:
                    # Ensure required keys exist; apply basic defaults
                    defect_type = data.get("defect_type", "no_defect")
                    severity_score = float(data.get("severity_score", 0))
                    condition_label = data.get("condition_label") or self.determine_condition(
                        severity_score
                    )
                    ai_confidence = float(data.get("ai_confidence", 0.9))
                    maintenance_suggestion = data.get("maintenance_suggestion", "").strip()

                    # For now we don't have Gemini-drawn annotations; reuse original image
                    original_img, _ = self.preprocess_image(image_path)
                    detections = {
                        "defect_type": defect_type,
                        "severity_score": severity_score,
                        "confidence": ai_confidence,
                    }
                    annotated_img = self.create_annotated_image(original_img, detections)

                    annotated_path = None
                    if annotated_img is not None:
                        annotated_dir = settings.MEDIA_ROOT / "annotated_images"
                        annotated_dir.mkdir(parents=True, exist_ok=True)

                        image_name = Path(image_path).stem
                        annotated_path = annotated_dir / f"{image_name}_annotated.jpg"
                        cv2.imwrite(str(annotated_path), annotated_img)

                    return {
                        "defect_type": defect_type,
                        "severity_score": severity_score,
                        "condition_label": condition_label,
                        "ai_confidence": ai_confidence,
                        "model_name": "Gemini 1.5 Flash",
                        "model_version": "1.0",
                        "analysis_metadata": data,
                        "annotated_image_path": str(annotated_path) if annotated_path else None,
                        "maintenance_suggestion": maintenance_suggestion,
                    }

            # Fallback: existing simple detector
            logger.info("Using simple OpenCV detector for road defect analysis")
            original_img, processed_img = self.preprocess_image(image_path)

            detections = self.detect_defects(processed_img)
            condition = self.determine_condition(detections["severity_score"])

            annotated_img = self.create_annotated_image(original_img, detections)

            annotated_path = None
            if annotated_img is not None:
                annotated_dir = settings.MEDIA_ROOT / "annotated_images"
                annotated_dir.mkdir(parents=True, exist_ok=True)

                image_name = Path(image_path).stem
                annotated_path = annotated_dir / f"{image_name}_annotated.jpg"
                cv2.imwrite(str(annotated_path), annotated_img)

            return {
                "defect_type": detections["defect_type"],
                "severity_score": detections["severity_score"],
                "condition_label": condition,
                "ai_confidence": detections["confidence"],
                "model_name": self.model_name,
                "model_version": self.model_version,
                "analysis_metadata": detections.get("metadata", {}),
                "annotated_image_path": str(annotated_path) if annotated_path else None,
            }

        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {str(e)}")
            raise


# Singleton instance
_detector_instance = None


def get_detector():
    """Get or create the detector instance"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = RoadDefectDetector()
        _detector_instance.load_model()
    return _detector_instance
