from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from backend.tools.s3_connector import *
from django.db.models import Count, Value
from django.db.models.functions import TruncDate

from ..models import CSVData


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
        data = []

        fields = CSVData._meta.fields
        field_names = [field.verbose_name for field in fields]
        attribute_names = [field.name for field in fields]

        for item in csv_data:
            item_data = {}
            for field_name, attribute_name in zip(field_names, attribute_names):
                field_value = getattr(item, attribute_name)
                item_data[field_name] = field_value
            data.append(item_data)

        return Response(data)
    except Exception as e:
        error_message = str(e)
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def s3_files_bucket_list_view(request):
    # try using channels to see files in real time?

    s3_connector = S3Connector(bucket_name="cb-silver-bucket")
    s3_files = s3_connector.get_csv_objects_in_dataset()

    db_files = CSVData.objects.values_list('file_name', flat=True)

    data = []
    for file in s3_files:
        file['is_in_db'] = file['file_name'] in db_files
        data.append(file)

    return Response(data)


@api_view(['POST'])
def upload_data_from_list_view(request):
    s3_connector = S3Connector(bucket_name="cb-silver-bucket")
    selected_files = request.data.get('files', [])
    filename_list = [file['file_name'] for file in selected_files]
    df, result_messages = s3_connector.read_csv_file_list(filename_list)

    # Print the DataFrame
    print("Combined DataFrame:")
    if not df.empty:
        num_files, num_lines = CSVData.objects.bulk_insert_from_csv(df)
        print(num_files, num_lines)

    # Print the error messages
    print("Messages:")
    print(result_messages)

    return Response(result_messages)


@api_view(['GET'])
def database_metadata(request):
    total_files = CSVData.objects.values('file_name').distinct().count()
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
    total_files_db = CSVData.objects.values('file_name').distinct().count()

    data = {
        's3_total_files': total_files_s3,
        'db_total_files': total_files_db
    }

    print(data)

    return Response(data)


@api_view(['GET'])
def timeline_data_view(request):
    data = CSVData.objects.annotate(date=TruncDate('creation_datetime')).values('date').annotate(
        file_count=Count('file_name', distinct=True),
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
            CSVData.objects.filter(file_name=file_name).delete()

            deleted_files_response.append({
                'status': 'ok',
                'file_name': file_name,
                'message': 'File data successfully deleted.'
            })

        return Response(deleted_files_response)
    else:
        return Response({'message': 'No files selected for deletion.'})
