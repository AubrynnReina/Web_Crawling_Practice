def load(ti):

    import pandas as pd
    # import boto3
    # import os
    # from dotenv import load_dotenv

    # # Get the credentials
    # load_dotenv()
    # AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    # AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

    # s3 = boto3.client(
    #     service_name='s3',
    #     region_name='ap-southeast-1',
    #     aws_access_key_id=AWS_ACCESS_KEY,
    #     aws_secret_access_key=AWS_SECRET_KEY
    # )
    
    # # Read the csv file from AWS S3 cloud
    # bucket='aub-demo'
    # objs_contents = s3.list_objects_v2(Bucket=bucket, Prefix='csv_data')['Contents']
    # obj_key = max(objs_contents, key=lambda x: x['LastModified'])['Key']
    # data = s3.get_object(Bucket=bucket, Key=obj_key)
    # contents = data['Body'].read().decode('utf-8')
    # print(contents)

    # Read the csv file locally
    FILE_NAME = ti.xcom_pull(key='file_name', task_ids='extract')
    df = pd.read_csv('data/csv_data/' + FILE_NAME + '.csv')