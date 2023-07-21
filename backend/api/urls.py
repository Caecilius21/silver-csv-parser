from django.urls import path
from . import views


urlpatterns = [
    # data inserted from csv files
    path('csv-data/', views.csv_data_view, name='csv_data_view'),
    # files in the s3 bucket
    path('s3-bucket-files-list/', views.s3_files_bucket_list_view),
    path('upload-data-from-list/', views.upload_data_from_list_view),
    path('database-metadata/', views.database_metadata),
    path('s3-vs-database-comparison/', views.s3_vs_database_comparison),
    path('timeline-data/', views.timeline_data_view),
    path('delete-files-from-database/', views.delete_files_from_database),
    path('ingestion-message-list/', views.ingestion_message_view),
]
