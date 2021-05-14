import boto3
from botocore.config import Config

from src.config.config import S3_KEY, S3_SECRET, S3_REGION


class ClientManager:
    def __init__(self, signature=None, addressing_style=None, credentials=None, endpoint=None):
        self._signature = signature if signature is not None else 's3v4'
        self._key = credentials.get('Key') if credentials is not None else S3_KEY
        self._secret = credentials.get('Secret') if credentials is not None else S3_SECRET
        self._addressing_style = addressing_style if addressing_style is not None else 'virtual'
        self._endpoint_url = endpoint if endpoint is not None else 'https://s3.amazonaws.com'

    def get_client(self):
        session = boto3.session.Session()

        kwargs = {'region_name': S3_REGION, 'service_name': 's3', 'aws_access_key_id': self._key,
                  'aws_secret_access_key': self._secret, 'endpoint_url': self._endpoint_url,
                  'config': Config(signature_version=self._signature,
                                   s3={'addressing_style': self._addressing_style},
                                   retries={'max_attempts': 0}), 'verify': False}

        s3 = session.client(**kwargs)

        return s3
