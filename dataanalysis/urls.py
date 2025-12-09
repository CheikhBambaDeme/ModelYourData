"""
URL patterns for the DataAnalysis app.
"""

from django.urls import path
from . import views

app_name = 'dataanalysis'

urlpatterns = [
    # Landing page with file upload
    path('', views.landing_page, name='landing'),
    
    # Upload endpoint (AJAX)
    path('upload/', views.upload_file, name='upload'),
    
    # Analysis page
    path('analysis/<uuid:file_id>/', views.analysis_page, name='analysis'),
    
    # API endpoints for analysis operations
    path('api/table/<uuid:file_id>/', views.api_table_preview, name='api_table'),
    path('api/linear-regression/<uuid:file_id>/', views.api_linear_regression, name='api_linear_regression'),
    path('api/clustering/<uuid:file_id>/', views.api_clustering, name='api_clustering'),
    path('api/distribution/<uuid:file_id>/', views.api_distribution, name='api_distribution'),
    path('api/statistics/<uuid:file_id>/', views.api_statistics, name='api_statistics'),
    path('api/eda/<uuid:file_id>/', views.api_eda_report, name='api_eda'),
    path('api/correlation/<uuid:file_id>/', views.api_correlation, name='api_correlation'),
    path('api/scatter/<uuid:file_id>/', views.api_scatter, name='api_scatter'),
    path('api/histogram/<uuid:file_id>/', views.api_histogram, name='api_histogram'),
    path('api/boxplot/<uuid:file_id>/', views.api_boxplot, name='api_boxplot'),
    
    # Download endpoint
    path('download/<uuid:file_id>/', views.download_visualization, name='download'),
    
    # Get columns for a file
    path('api/columns/<uuid:file_id>/', views.api_get_columns, name='api_columns'),
]
