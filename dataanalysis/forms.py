"""
Forms for the DataAnalysis app.
Handles CSV file upload validation.
"""

from django import forms
from .models import UploadedFile


class CSVUploadForm(forms.Form):
    """
    Form for uploading CSV files.
    Validates file type and size.
    """
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Maximum file size: 10MB',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class': 'file-input',
            'id': 'csv-file-input',
        })
    )
    
    def clean_csv_file(self):
        """Validate the uploaded CSV file."""
        file = self.cleaned_data.get('csv_file')
        
        if file:
            # Check file extension
            if not file.name.endswith('.csv'):
                raise forms.ValidationError('Only CSV files are allowed.')
            
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 10MB.')
            
            # Check if file is not empty
            if file.size == 0:
                raise forms.ValidationError('The uploaded file is empty.')
        
        return file


class AnalysisParametersForm(forms.Form):
    """
    Form for specifying analysis parameters.
    Used for operations that require column selection or other parameters.
    """
    x_column = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    y_column = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    n_clusters = forms.IntegerField(
        required=False,
        min_value=2,
        max_value=10,
        initial=3,
        widget=forms.NumberInput(attrs={'class': 'form-input', 'min': 2, 'max': 10})
    )
