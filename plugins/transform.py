def transform(ti):

    import json
    import pandas as pd
    import boto3
    from io import StringIO
    import os
    from dotenv import load_dotenv

    # Get the credentials then the json file
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

    s3 = boto3.client(
        service_name='s3',
        region_name='ap-southeast-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    bucket='aub-demo'
    # objs_contents = s3.list_objects_v2(Bucket=bucket, Prefix='json_data')['Contents']
    # obj_key = max(objs_contents, key=lambda x: x['LastModified'])['Key']
    # data = s3.get_object(Bucket=bucket, Key=obj_key)
    # contents = data['Body'].read().decode('utf-8')

    # json_data = json.loads(contents)

    # Get the json file locally
    FILE_NAME = ti.xcom_pull(key='file_name', task_ids='extract')
    JSON_DATA_PATH = 'data/json_data/' + FILE_NAME + '.json'
    f = open(JSON_DATA_PATH, 'r+', encoding='utf-8')
    json_data = json.load(f)
    # Read the json file
    ids = []
    names = []
    prices = []
    discount_rates = []

    for i in range(len(json_data['data'])):
        ids.append(json_data['data'][i]['id'])
        names.append(json_data['data'][i]['name'])
        prices.append(json_data['data'][i]['price'])
        discount_rates.append(json_data['data'][i]['discount_rate'])

    # Put the lists into a csv file and load to AWS S3
    save_df = pd.DataFrame(data=zip(ids, names, prices, discount_rates), columns=['id', 'name', 'price', 'discount_rate'])
    buffer_csv = StringIO()
    save_df.to_csv(buffer_csv, header=True, index=False)
    s3.put_object(Bucket=bucket, Body=buffer_csv.getvalue(), Key='csv_data/' + FILE_NAME + '.csv')

    # Save the csv file locally
    CSV_DATA_PATH = 'data/csv_data/' + FILE_NAME + '.csv'
    save_df.to_csv(CSV_DATA_PATH, header=True, index=False)
