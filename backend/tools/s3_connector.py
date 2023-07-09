import boto3
import pandas as pd


class S3Connector:
    def __init__(self,
                 aws_access_key_id,
                 aws_secret_access_key,
                 region_name="eu-west-1",
                 bucket_name="cb-silver-bucket",
                 dataset="csv-data"):
        self.bucket_name = bucket_name
        self.dataset = dataset
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def get_total_files_in_dataset(self):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=self.dataset)
            total_files = response['KeyCount'] - 1
            return total_files
        except Exception as e:
            print(f"Error fetching total files from S3: {e}")
            return None

    def get_csv_objects_in_dataset(self, existing_files=[]):
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name, Prefix=self.dataset)

        csv_objects = []

        if 'Contents' in response:
            objects = response['Contents']
            csv_objects = [
                {
                    'file_name': obj['Key'],
                    'size': obj['Size'],
                    'creation_date': obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S"),
                    'etag': obj['ETag'],
                    'storage_class': obj['StorageClass']
                }
                for obj in objects
                if obj['Key'].lower().endswith('.csv') and obj['Key'] not in existing_files
            ]

        return csv_objects

    def read_csv(self, file_name):
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=file_name)
            content = response['Body']
            df = pd.read_csv(content)

            required_columns = ["username", "address", "description", "email"]
            alt_required_columns = [
                "nom d'utilisateur", "adresse", "Text de description", "adresse mail"]

            if not set(required_columns).issubset(df.columns) and not set(alt_required_columns).issubset(df.columns):
                error_message = f"CSV file {file_name} does not have the required columns."
                return pd.DataFrame(), {'status': 'ko', 'file_name': file_name, 'message': error_message}

            column_mapping = dict(zip(df.columns, required_columns))
            df = df.rename(columns=column_mapping)
            df['file_name'] = file_name
            return df, {'status': 'ok', 'file_name': file_name, 'message': "File data successfully uploaded."}
        except Exception as e:
            error_message = f"Error reading CSV from S3: {e}"
            return pd.DataFrame(), {'status': 'ko', 'file_name': file_name, 'message': error_message}

    def read_csv_file_list(self, filename_list):
        data = []
        result_messages = []
        for file_name in filename_list:
            df, result = self.read_csv(file_name)
            if not df.empty:
                data.append(df)
            result_messages.append(result)

        if not data:
            combined_df = pd.DataFrame()
        else:
            combined_df = pd.concat(data, ignore_index=True)

        return combined_df, result_messages
