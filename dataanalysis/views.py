"""
Views for the DataAnalysis app.
Handles file upload, analysis operations, and visualization rendering.
"""

import io
import json
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from .models import UploadedFile, AnalysisResult
from .forms import CSVUploadForm
from .utils.analysis import (
    load_csv,
    generate_table_preview,
    perform_linear_regression,
    perform_clustering,
    generate_distribution_plot,
    generate_statistical_summary,
    generate_eda_report,
    generate_correlation_matrix,
    generate_scatter_plot,
    generate_histogram,
    generate_boxplot,
    get_numeric_columns,
    get_categorical_columns,
)


def landing_page(request):
    """
    Render the landing page with file upload form.
    """
    form = CSVUploadForm()
    return render(request, 'dataanalysis/landing.html', {'form': form})


@require_http_methods(["POST"])
def upload_file(request):
    """
    Handle CSV file upload via AJAX.
    Returns JSON with file_id for redirection.
    """
    form = CSVUploadForm(request.POST, request.FILES)
    
    if form.is_valid():
        csv_file = form.cleaned_data['csv_file']
        
        # Create UploadedFile instance
        uploaded_file = UploadedFile(
            file=csv_file,
            original_filename=csv_file.name,
            file_size=csv_file.size
        )
        uploaded_file.save()
        
        return JsonResponse({
            'success': True,
            'file_id': str(uploaded_file.id),
            'redirect_url': f'/analysis/{uploaded_file.id}/'
        })
    else:
        errors = {field: errors for field, errors in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)


def analysis_page(request, file_id):
    """
    Render the analysis page for a specific uploaded file.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # Load the CSV and get column information
    try:
        df = load_csv(uploaded_file.file.path)
        numeric_columns = get_numeric_columns(df)
        categorical_columns = get_categorical_columns(df)
        all_columns = df.columns.tolist()
    except Exception as e:
        return render(request, 'dataanalysis/error.html', {'error': str(e)})
    
    context = {
        'file': uploaded_file,
        'numeric_columns': numeric_columns,
        'categorical_columns': categorical_columns,
        'all_columns': all_columns,
    }
    
    return render(request, 'dataanalysis/analysis.html', context)


@require_http_methods(["GET"])
def api_table_preview(request, file_id):
    """
    API endpoint to get table preview.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        max_rows = int(request.GET.get('max_rows', 20))
        result = generate_table_preview(df, max_rows)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_linear_regression(request, file_id):
    """
    API endpoint for linear regression analysis.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        x_column = data.get('x_column')
        y_column = data.get('y_column')
        
        result = perform_linear_regression(df, x_column, y_column)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_clustering(request, file_id):
    """
    API endpoint for clustering analysis.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        n_clusters = int(data.get('n_clusters', 3))
        columns = data.get('columns')
        if isinstance(columns, str):
            columns = columns.split(',') if columns else None
        
        result = perform_clustering(df, n_clusters, columns)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_distribution(request, file_id):
    """
    API endpoint for distribution plot.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        column = data.get('column')
        
        result = generate_distribution_plot(df, column)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def api_statistics(request, file_id):
    """
    API endpoint for statistical summary.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        result = generate_statistical_summary(df)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def api_eda_report(request, file_id):
    """
    API endpoint for full EDA report.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        result = generate_eda_report(df)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def api_correlation(request, file_id):
    """
    API endpoint for correlation matrix.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        result = generate_correlation_matrix(df)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_scatter(request, file_id):
    """
    API endpoint for scatter plot.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        x_column = data.get('x_column')
        y_column = data.get('y_column')
        
        result = generate_scatter_plot(df, x_column, y_column)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_histogram(request, file_id):
    """
    API endpoint for histogram.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        column = data.get('column')
        bins = int(data.get('bins', 30))
        
        result = generate_histogram(df, column, bins)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def api_boxplot(request, file_id):
    """
    API endpoint for box plot.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        
        # Get parameters
        if request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
        else:
            data = request.GET
        
        columns = data.get('columns')
        if isinstance(columns, str):
            columns = columns.split(',') if columns else None
        
        result = generate_boxplot(df, columns)
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def api_get_columns(request, file_id):
    """
    API endpoint to get column information for a file.
    """
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    try:
        df = load_csv(uploaded_file.file.path)
        result = {
            'numeric_columns': get_numeric_columns(df),
            'categorical_columns': get_categorical_columns(df),
            'all_columns': df.columns.tolist()
        }
        return JsonResponse({'success': True, 'data': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET", "POST"])
def download_visualization(request, file_id):
    """
    Download the current visualization as PNG.
    Expects base64 image data in POST request.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data', '')
            filename = data.get('filename', 'visualization.png')
            format_type = data.get('format', 'png')
            
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Create response
            content_types = {
                'png': 'image/png',
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'pdf': 'application/pdf'
            }
            
            content_type = content_types.get(format_type, 'image/png')
            
            response = HttpResponse(image_bytes, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
