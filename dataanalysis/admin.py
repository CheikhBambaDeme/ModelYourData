from django.contrib import admin
from .models import UploadedFile, AnalysisResult


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'uploaded_at', 'file_size', 'id')
    list_filter = ('uploaded_at',)
    search_fields = ('original_filename',)
    readonly_fields = ('id', 'uploaded_at')


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('operation', 'uploaded_file', 'created_at', 'id')
    list_filter = ('operation', 'created_at')
    search_fields = ('uploaded_file__original_filename',)
    readonly_fields = ('id', 'created_at')
