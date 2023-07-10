from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.tools.s3_connector import *
from django.db.models import Count
from django.db.models.functions import TruncDate

from ..models import CSVData, File, IngestionMessage
from .serializers import CSVDataSerializer, IngestionMessageSerializer


@api_view(['GET'])
def csv_data_view(request):
    """
    Retrieve and serialize all instances of CSVData.

    This view function handles a GET request and retrieves all instances of the CSVData model. 
    The retrieved data is processed and serialized into a list of dictionaries,
    where each dictionary represents a single instance of CSVData with field names as keys and their respective values.

    Returns:
        Response: A response object containing the serialized CSVData instances as a list of dictionaries.

    Raises:
        Exception: If an error occurs during data retrieval or serialization, 
        an error message is returned as a JSON response with a status code of 500 (Internal Server Error).
    """

    try:
        csv_data = CSVData.objects.all()
        serializer = CSVDataSerializer(csv_data, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_message = str(e)
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def s3_files_bucket_list_view(request):
    """
    Retrieve a list of files from an S3 bucket and check if they exist in the File model.

    This API view connects to an S3 bucket and retrieves a list of files in the bucket.
    It then checks each file against the File model to determine if it already exists in the database.
    If a file doesn't exist in the File model, a new File instance is created.

    Returns:
        A Response object containing a list of files with additional information:
            - 'file_name': Name of the file.
            - 'size': Size of the file.
            - 'creation_date': Creation date of the file.
            - 'bucket': Bucket name of the file.
            - 'is_in_db': Boolean indicating if the file exists in the File model.
    """
    s3_connector = S3Connector()
    s3_files = s3_connector.get_csv_objects_in_dataset()

    db_files = CSVData.objects.values_list('file__file_name', flat=True)

    data = []
    for file in s3_files:
        file['is_in_db'] = file['file_name'] in db_files

        file_instance, created = File.objects.get_or_create(
            file_name=file['file_name'],
            defaults={
                'size': file['size'],
                'creation_datetime': file['creation_date'],
                'bucket': s3_connector.bucket_name
            })
        print(file_instance.file_name, created)

        data.append(file)

    return Response(data)


@api_view(['POST'])
def upload_data_from_list_view(request):
    s3_connector = S3Connector(bucket_name="cb-silver-bucket")
    selected_files = request.data.get('files', [])
    filename_list = [file['file_name'] for file in selected_files]
    df, result_messages = s3_connector.read_csv_file_list(filename_list)

    print("Combined DataFrame:")
    if not df.empty:
        existing_files = CSVData.objects.filter(
            file__file_name__in=filename_list).values_list('file__file_name', flat=True)
        new_files_df = df[~df['file_name'].isin(existing_files)]
        if not new_files_df.empty:
            num_files, num_lines = CSVData.objects.bulk_insert_from_csv(
                new_files_df)
            print(num_files, num_lines)

            for message in result_messages:
                status = message['status']
                if status == 'ko':
                    num_lines = 0
                IngestionMessage.objects.create(
                    file=File.objects.get(file_name=message['file_name']),
                    status=status,
                    message=message['message'],
                    num_lines=num_lines
                )

    print("Messages:")
    print(result_messages)

    return Response(result_messages)


@api_view(['GET'])
def database_metadata(request):
    total_files = CSVData.objects.values('file__file_name').distinct().count()
    total_unique_data = CSVData.objects.distinct().count()
    print(total_files, total_unique_data)

    metadata = {
        'total_unique_files': total_files,
        'total_data': total_unique_data
    }

    return Response(metadata)


@api_view(['GET'])
def s3_vs_database_comparison(request):
    s3_connector = S3Connector(bucket_name="cb-silver-bucket")
    total_files_s3 = s3_connector.get_total_files_in_dataset()
    total_files_db = CSVData.objects.values(
        'file__file_name').distinct().count()

    data = {
        's3_total_files': total_files_s3,
        'db_total_files': total_files_db
    }

    print(data)

    return Response(data)


@api_view(['GET'])
def timeline_data_view(request):
    data = CSVData.objects.annotate(date=TruncDate('ingestion_datetime')).values('date').annotate(
        file_count=Count('file__file_name', distinct=True),
        row_count=Count('id')
    ).order_by('date')

    files = [[entry['date'], entry['file_count']] for entry in data]
    rows = [[entry['date'], entry['row_count']] for entry in data]

    return Response({
        'files': files,
        'rows': rows
    })


@api_view(['POST'])
def delete_files_from_database(request):
    files = request.data.get('files', [])

    if files:
        deleted_files_response = []

        for file in files:
            file_name = file['file_name']
            CSVData.objects.filter(file__file_name=file_name).delete()

            deleted_files_response.append({
                'status': 'ok',
                'file_name': file_name,
                'message': 'File data successfully deleted.'
            })

        return Response(deleted_files_response)
    else:
        return Response({'message': 'No files selected for deletion.'})


@api_view(['GET'])
def ingestion_message_view(request):
    """
    Retrieve and serialize all instances of IngestionMessage.

    This view function handles a GET request and retrieves all instances of the IngestionMessage model. 
    The retrieved data is processed and serialized into a list of dictionaries,
    where each dictionary represents a single instance of IngestionMessage with field names as keys and their respective values.

    Returns:
        Response: A response object containing the serialized IngestionMessage instances as a list of dictionaries.

    Raises:
        Exception: If an error occurs during data retrieval or serialization, 
        an error message is returned as a JSON response with a status code of 500 (Internal Server Error).
    """

    try:
        ingestion_messages = IngestionMessage.objects.all()
        serializer = IngestionMessageSerializer(ingestion_messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_message = str(e)
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
