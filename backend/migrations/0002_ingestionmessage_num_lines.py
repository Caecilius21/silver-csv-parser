# Generated by Django 3.2 on 2023-07-09 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestionmessage',
            name='num_lines',
            field=models.TextField(default=0, verbose_name='Nombre de lignes'),
            preserve_default=False,
        ),
    ]
