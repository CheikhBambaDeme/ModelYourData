"""
Models for the DataAnalysis app.
Handles storage of uploaded CSV files and analysis sessions.
"""

import uuid
from django.db import models


class UploadedFile(models.Model):
    """
    Model to store uploaded CSV files.
    Uses UUID for unique identification and secure file access.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(default=0)  # Size in bytes
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} ({self.id})"
    
    def delete(self, *args, **kwargs):
        """Delete the file from storage when model is deleted."""
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


class AnalysisResult(models.Model):
    """
    Model to store analysis results/visualizations.
    Links to the uploaded file and stores the generated plot.
    """
    OPERATION_CHOICES = [
        ('table', 'Data Table Preview'),
        ('linear_regression', 'Linear Regression'),
        ('clustering', 'Clustering (KMeans)'),
        ('distribution', 'Distribution Plot'),
        ('statistical_summary', 'Statistical Summary'),
        ('eda_report', 'Full EDA Report'),
        ('correlation', 'Correlation Matrix'),
        ('scatter', 'Scatter Plot'),
        ('histogram', 'Histogram'),
        ('boxplot', 'Box Plot'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_file = models.ForeignKey(
        UploadedFile, 
        on_delete=models.CASCADE, 
        related_name='analysis_results'
    )
    operation = models.CharField(max_length=50, choices=OPERATION_CHOICES)
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)
    result_html = models.TextField(null=True, blank=True)  # For table/summary HTML
    created_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField(default=dict, blank=True)  # Store operation parameters
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.operation} - {self.uploaded_file.original_filename}"
    
    def delete(self, *args, **kwargs):
        """Delete the result image from storage when model is deleted."""
        if self.result_image:
            self.result_image.delete(save=False)
        super().delete(*args, **kwargs)
