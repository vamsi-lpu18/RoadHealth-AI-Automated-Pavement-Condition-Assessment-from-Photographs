"""
PDF Report Generator for Road Analysis

Uses ReportLab to create professional PDF reports with analysis results.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
import os


class PDFReportGenerator:
    """Generate PDF reports for road condition analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        styles = {}
        
        # Title style
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Heading style
        styles['CustomHeading'] = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Normal text
        styles['CustomNormal'] = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=8,
        )
        
        return styles
    
    def generate_report(self, image_record, analysis_result):
        """
        Generate PDF report for a single image analysis.
        
        Args:
            image_record: ImageRecord instance
            analysis_result: AnalysisResult instance
            
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add logo/header (if available)
        elements.append(Paragraph("RoadHealth AI", self.custom_styles['CustomTitle']))
        elements.append(Paragraph("Road Condition Analysis Report", self.styles['Heading2']))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%B %d, %Y %I:%M %p')],
            ['Report ID:', f"RH-{image_record.id:06d}"],
            ['', ''],
        ]
        
        t = Table(metadata, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Image Information Section
        elements.append(Paragraph("Image Information", self.custom_styles['CustomHeading']))
        
        image_info = [
            ['Uploaded By:', image_record.user.get_full_name() or image_record.user.email],
            ['Upload Date:', image_record.upload_date.strftime('%B %d, %Y %I:%M %p')],
            ['Title:', image_record.title or 'N/A'],
            ['Description:', image_record.description or 'N/A'],
        ]
        
        if image_record.has_location:
            image_info.extend([
                ['Location:', image_record.location_name or 'Not specified'],
                ['Coordinates:', f"{image_record.latitude}, {image_record.longitude}"],
            ])
        
        t = Table(image_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Analysis Results Section
        elements.append(Paragraph("Analysis Results", self.custom_styles['CustomHeading']))
        
        # Condition color coding
        condition_colors = {
            'good': colors.green,
            'moderate': colors.orange,
            'poor': colors.orangered,
            'critical': colors.red,
        }
        
        condition_color = condition_colors.get(analysis_result.condition_label, colors.grey)
        
        analysis_info = [
            ['Defect Type:', analysis_result.get_defect_type_display()],
            ['Severity Score:', f"{analysis_result.severity_score:.2f} / 100"],
            ['Condition:', analysis_result.get_condition_label_display().upper()],
            ['AI Confidence:', f"{analysis_result.ai_confidence * 100:.1f}%"],
            ['Model Used:', f"{analysis_result.model_name} v{analysis_result.model_version}"],
            ['Analysis Date:', analysis_result.analyzed_at.strftime('%B %d, %Y %I:%M %p')],
        ]
        
        t = Table(analysis_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('TEXTCOLOR', (1, 2), (1, 2), condition_color),  # Condition row
            ('FONT', (1, 2), (1, 2), 'Helvetica-Bold', 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Maintenance Recommendation
        elements.append(Paragraph("Maintenance Recommendation", self.custom_styles['CustomHeading']))
        elements.append(Paragraph(analysis_result.maintenance_suggestion, self.custom_styles['CustomNormal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Add images if available
        try:
            if os.path.exists(image_record.image.path):
                elements.append(Paragraph("Original Image", self.custom_styles['CustomHeading']))
                img = Image(image_record.image.path, width=5*inch, height=3.5*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.2 * inch))
        except:
            pass
        
        try:
            if analysis_result.annotated_image and os.path.exists(analysis_result.annotated_image.path):
                elements.append(Paragraph("Annotated Analysis Image", self.custom_styles['CustomHeading']))
                img = Image(analysis_result.annotated_image.path, width=5*inch, height=3.5*inch)
                elements.append(img)
        except:
            pass
        
        # Footer
        elements.append(PageBreak())
        footer_text = """
        <para alignment="center">
        <b>RoadHealth AI - Automated Pavement Condition Assessment</b><br/>
        This report is generated automatically by AI analysis and should be reviewed by qualified engineers.<br/>
        For questions or concerns, please contact your system administrator.
        </para>
        """
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
    
    def generate_summary_report(self, image_records, analysis_results):
        """
        Generate summary PDF report for multiple analyses.
        
        Args:
            image_records: QuerySet of ImageRecord instances
            analysis_results: QuerySet of AnalysisResult instances
            
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        elements = []
        
        # Title
        elements.append(Paragraph("RoadHealth AI Summary Report", self.custom_styles['CustomTitle']))
        elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", 
                                 self.styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))
        
        # Summary statistics
        total = analysis_results.count()
        critical = analysis_results.filter(condition_label='critical').count()
        poor = analysis_results.filter(condition_label='poor').count()
        moderate = analysis_results.filter(condition_label='moderate').count()
        good = analysis_results.filter(condition_label='good').count()
        
        summary_data = [
            ['Condition', 'Count', 'Percentage'],
            ['Critical', str(critical), f"{(critical/total*100):.1f}%" if total > 0 else "0%"],
            ['Poor', str(poor), f"{(poor/total*100):.1f}%" if total > 0 else "0%"],
            ['Moderate', str(moderate), f"{(moderate/total*100):.1f}%" if total > 0 else "0%"],
            ['Good', str(good), f"{(good/total*100):.1f}%" if total > 0 else "0%"],
            ['Total', str(total), '100%'],
        ]
        
        t = Table(summary_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Detailed records
        elements.append(Paragraph("Detailed Records", self.custom_styles['CustomHeading']))
        
        record_data = [['ID', 'Location', 'Defect', 'Condition', 'Severity']]
        
        for analysis in analysis_results[:50]:  # Limit to 50 records
            record_data.append([
                str(analysis.image_record.id),
                analysis.image_record.location_name[:20] if analysis.image_record.location_name else 'N/A',
                analysis.get_defect_type_display()[:15],
                analysis.get_condition_label_display(),
                f"{analysis.severity_score:.1f}",
            ])
        
        t = Table(record_data, colWidths=[0.7*inch, 2*inch, 1.5*inch, 1*inch, 1*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(t)
        
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
