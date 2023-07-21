from django.test import TestCase
from backend.models import File, CSVData, IngestionMessage
from django.utils import timezone

class ModelTests(TestCase):
    def setUp(self):
        pass

    def test_file_model(self):
        # Test the File model
        file = File.objects.create(
            file_name='test_file.txt',
            size=1024,
            creation_datetime='2023-07-21 12:00:00',
            bucket='test_bucket'
        )
        self.assertEqual(str(file), 'test_file.txt')
        self.assertEqual(file.size, 1024)
        self.assertEqual(str(file.creation_datetime), '2023-07-21 12:00:00')
        self.assertEqual(file.bucket, 'test_bucket')

    def test_csv_data_model(self):
        # Test the CSVData model
        file = File.objects.create(
            file_name='test_file.txt',
            size=1024,
            creation_datetime='2023-07-21 12:00:00',
            bucket='test_bucket'
        )
        csv_data = CSVData.objects.create(
            username='test_user',
            address='test_address',
            description='test_description',
            email='test@example.com',
            file=file
        )
        self.assertEqual(str(csv_data), 'test_user')
        self.assertEqual(csv_data.username, 'test_user')
        self.assertEqual(csv_data.address, 'test_address')
        self.assertEqual(csv_data.description, 'test_description')
        self.assertEqual(csv_data.email, 'test@example.com')
        self.assertEqual(csv_data.file, file)

    def test_ingestion_message_model(self):
        # Test the IngestionMessage model
        file = File.objects.create(
            file_name='test_file.txt',
            size=1024,
            creation_datetime=timezone.now(),
            bucket='test_bucket'
        )
        ingestion_timestamp = timezone.now()
        ingestion_message = IngestionMessage.objects.create(
            file=file,
            status='ok',
            message='Test message',
            num_lines='10',
            ingestion_timestamp=ingestion_timestamp
        )
        self.assertEqual(str(ingestion_message), 'Test message')
        self.assertEqual(ingestion_message.file, file)
        self.assertEqual(ingestion_message.status, 'ok')
        self.assertEqual(ingestion_message.message, 'Test message')
        self.assertEqual(ingestion_message.num_lines, '10')
        self.assertEqual(
            ingestion_message.ingestion_timestamp,
            ingestion_timestamp
        )
