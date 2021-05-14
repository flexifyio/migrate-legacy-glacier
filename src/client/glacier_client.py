import boto3
from botocore.config import Config

from config.config import GL_KEY, GL_SECRET, GL_REGION


class GlacierClient:
    def __init__(self):
        pass

    def get_client(self):
        kwargs = {
            'service_name': 'glacier',
            'aws_access_key_id': GL_KEY,
            'aws_secret_access_key': GL_SECRET,
            'config': Config(region_name=GL_REGION)
        }

        return boto3.client(**kwargs)
