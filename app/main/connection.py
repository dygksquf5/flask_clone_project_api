from urllib.parse import urlparse

import requests

from .config import S3_CONFIG, KAKAO_CONFIG

import boto3


# s3
def connect_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=S3_CONFIG.S3_ACCESS_KEY,
        aws_secret_access_key=S3_CONFIG.S3_SECRET_KEY
    )
    return s3


def upload_s3(s3, picture, filename):
    s3.upload_fileobj(
        picture,
        S3_CONFIG.S3_BUCKET,
        filename
    )
    image_url = f"{S3_CONFIG.S3_BUCKET_URL}{filename}"
    return image_url


# kakao

def get_kakao(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?&query=' + address
    result = requests.get(urlparse(url).geturl(),
                          headers={'Authorization': 'KakaoAK ' + KAKAO_CONFIG.KAKAO_API_TOKEN}).json()
    match_first = result['documents'][0]['address']
    latitude = float(match_first['y'])
    longitude = float(match_first['x'])
    return latitude, longitude
