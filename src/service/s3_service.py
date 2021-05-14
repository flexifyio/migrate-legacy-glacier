from src.client.s3_client import ClientManager
from src.config.config import S3_BUCKET
from src.service.custom_multipart_upload import CustomMultipart


class S3Service:
    def __init__(self):
        self._client = ClientManager().get_client()
        self._bucket = S3_BUCKET
        self._multipart = CustomMultipart(self._client, self._bucket)

    def init_upload(self, key):
        self._multipart.init_multipart_upload(key)

    def upload_chunk(self, chunk):
        self._multipart.upload_next_chunk(chunk)

    def finish(self):
        self._multipart.complete_upload()

    def get_status(self):
        return self._multipart.get_status()