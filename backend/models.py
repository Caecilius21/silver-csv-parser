from django.db import models
from .managers import CSVDataManager


class File(models.Model):
    file_name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    creation_datetime = models.DateTimeField()
    bucket = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-creation_datetime']


class CSVData(models.Model):
    username = models.CharField(
        max_length=255, verbose_name="nom d'utilisateur")
    address = models.CharField(max_length=255, verbose_name="adresse")
    description = models.TextField(verbose_name="texte de description")
    email = models.EmailField(verbose_name="adresse mail")
    file = models.ForeignKey(
        File, on_delete=models.CASCADE, verbose_name="nom du fichier")
    ingestion_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="temps d'ingestion")

    objects = CSVDataManager()

    def __str__(self):
        return self.username


class IngestionMessage(models.Model):
    STATUS_CHOICES = [
        ('ok', 'ok'),
        ('ko', 'ko')
    ]

    file = models.ForeignKey(
        File, on_delete=models.CASCADE, verbose_name="nom du fichier")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="status")
    message = models.CharField(max_length=255, verbose_name="message")
    num_lines = models.TextField(verbose_name="Nombre de lignes")
    ingestion_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="temps d'ingestion")

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-ingestion_timestamp']
