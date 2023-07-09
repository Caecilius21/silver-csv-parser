from django.db import models
from .managers import CSVDataManager


class CSVData(models.Model):
    username = models.CharField(
        max_length=255, verbose_name="nom d'utilisateur")
    address = models.CharField(max_length=255, verbose_name="adresse")
    description = models.TextField(verbose_name="texte de description")
    email = models.EmailField(verbose_name="adresse mail")
    file_name = models.CharField(max_length=255, verbose_name="nom du fichier")
    creation_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="temps de création")

    objects = CSVDataManager()

    def __str__(self):
        return self.username
