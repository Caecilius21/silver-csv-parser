from rest_framework import serializers
from ..models import File, CSVData, IngestionMessage


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name']


class CSVDataSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source='file.file_name')

    class Meta:
        model = CSVData
        fields = [
            'id',
            'username',
            'address',
            'description',
            'email',
            'file_name',
            'ingestion_datetime',
        ]
        extra_kwargs = {
            'username': {'label': 'nom d\'utilisateur'},
            'address': {'label': 'adresse'},
            'description': {'label': 'texte de description'},
            'email': {'label': 'adresse mail'},
            'file_name': {'label': 'nom du fichier'},
            'ingestion_datetime': {'label': 'temps d\'ingestion'},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['file'] = instance.file.file_name
        return data


class IngestionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestionMessage
        fields = [
            'id',
            'file',
            'status',
            'message',
            'num_lines',
            'ingestion_timestamp',
        ]
        extra_kwargs = {
            'file': {'label': 'nom du fichier'},
            'status': {'label': 'status'},
            'message': {'label': 'message'},
            'num_lines': {'label': 'Nombre de lignes'},
            'ingestion_timestamp': {'label': 'temps d\'ingestion'},
        }
