def extract(ti):

    import requests
    from bs4 import BeautifulSoup
    import boto3
    import datetime
    import os
    from dotenv import load_dotenv
    # Access a web page
    # Nhà sách Tiki
    page_url = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=393b240b-204b-fb68-7b04-c26cdd32ea3d&category=8322&page=1&urlKey=nha-sach-tiki'

    header = {
        # 'authority': 'tiki.vn',
        # 'method': 'GET',
        # 'path': '/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=393b240b-204b-fb68-7b04-c26cdd32ea3d&category=8322&page=1&urlKey=nha-sach-tiki',
        # 'scheme': 'https',
        # 'Accept': 'application/json, text/plain, */*',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        # 'Accept-Language': 'en-US,en;q=0.7',
        # 'Cookie': '_trackity=393b240b-204b-fb68-7b04-c26cdd32ea3d; TKSESSID=8f2545b1a481f0357fb1a5afc8c0eb5d; delivery_zone=Vk4wMzkwMDYwMDE=; tiki_client_id=; TOKENS={%22access_token%22:%22F9jCpxvHtQr2KkXa8340GEVAmJZYnwfB%22%2C%22expires_in%22:157680000%2C%22expires_at%22:1875148066181%2C%22guest_token%22:%22F9jCpxvHtQr2KkXa8340GEVAmJZYnwfB%22}',
        # 'Priority': 'u=1, i',
        # 'Referer': 'https://tiki.vn/nha-sach-tiki/c8322',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    # Save the response
    page = requests.get(page_url, headers=header, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Upload to S3 Bucket
    current_time = datetime.datetime.now()
    FILE_NAME = str(current_time.strftime('%m-%d-%Y_%H-%M-%S')) + '_tiki_bookstore'

    ti.xcom_push(key='file_name', value=FILE_NAME)
    # Get the credentials
    load_dotenv()
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')

    s3 = boto3.client(
        service_name='s3',
        region_name='ap-southeast-1',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    bucket = 'aub-demo'
    s3.put_object(Bucket=bucket, Body=soup.text, Key= 'json_data/' + FILE_NAME + '.json')

    # Create a json file and save it locally
    JSON_DATA_PATH = 'data/json_data/' + FILE_NAME + '.json'
    with open(JSON_DATA_PATH, 'a+', encoding='utf-8') as f:
        f.write(soup.text)
