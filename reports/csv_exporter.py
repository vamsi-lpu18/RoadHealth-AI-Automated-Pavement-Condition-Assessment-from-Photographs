"""
CSV Export utilities for data export
"""

import csv
from io import StringIO
import pandas as pd
from datetime import datetime


def export_analysis_to_csv(analysis_results):
    """
    Export analysis results to CSV format.
    
    Args:
        analysis_results: QuerySet of AnalysisResult instances
        
    Returns:
        CSV string
    """
    # Create StringIO buffer
    output = StringIO()
    writer = csv.writer(output)
    
    # Write headers
    headers = [
        'ID',
        'Image ID',
        'User Email',
        'Upload Date',
        'Location',
        'Latitude',
        'Longitude',
        'Defect Type',
        'Severity Score',
        'Condition',
        'AI Confidence',
        'Model Name',
        'Model Version',
        'Maintenance Suggestion',
        'Analysis Date',
    ]
    writer.writerow(headers)
    
    # Write data
    for analysis in analysis_results:
        img = analysis.image_record
        row = [
            analysis.id,
            img.id,
            img.user.email,
            img.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            img.location_name or 'N/A',
            img.latitude or '',
            img.longitude or '',
            analysis.get_defect_type_display(),
            f"{analysis.severity_score:.2f}",
            analysis.get_condition_label_display(),
            f"{analysis.ai_confidence:.4f}",
            analysis.model_name,
            analysis.model_version,
            analysis.maintenance_suggestion,
            analysis.analyzed_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        writer.writerow(row)
    
    # Get CSV string
    csv_string = output.getvalue()
    output.close()
    
    return csv_string


def export_analysis_to_excel(analysis_results):
    """
    Export analysis results to Excel format using pandas.
    
    Args:
        analysis_results: QuerySet of AnalysisResult instances
        
    Returns:
        Excel file bytes
    """
    # Prepare data
    data = []
    
    for analysis in analysis_results:
        img = analysis.image_record
        data.append({
            'ID': analysis.id,
            'Image ID': img.id,
            'User Email': img.user.email,
            'Upload Date': img.upload_date,
            'Location': img.location_name or 'N/A',
            'Latitude': img.latitude,
            'Longitude': img.longitude,
            'Defect Type': analysis.get_defect_type_display(),
            'Severity Score': analysis.severity_score,
            'Condition': analysis.get_condition_label_display(),
            'AI Confidence': analysis.ai_confidence,
            'Model Name': analysis.model_name,
            'Model Version': analysis.model_version,
            'Maintenance Suggestion': analysis.maintenance_suggestion,
            'Analysis Date': analysis.analyzed_at,
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Analysis Results', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Analysis Results']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    excel_data = output.getvalue()
    output.close()
    
    return excel_data


from io import BytesIO
