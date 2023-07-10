from django.db import models
from django.apps import apps


class CSVDataManager(models.Manager):
    def bulk_insert_from_csv(self, data):
        File = apps.get_model('backend', 'File')

        num_files = data['file_name'].nunique()
        num_lines = len(data)

        mapped_data = [
            {
                'username': item['username'],
                'address': item['address'],
                'description': item['description'],
                'email': item['email'],
                'file': File.objects.get(file_name=item['file_name'])
            }
            for _, item in data.iterrows()
        ]
        objs = [self.model(**item) for item in mapped_data]

        self.bulk_create(objs)

        print(f"{num_files} file(s) with {num_lines} lines successfully bulk inserted into {self.model._meta.verbose_name_plural}.")
        return num_files, num_lines

    def get_file_names(self):
        return self.values_list('file__file_name', flat=True)
