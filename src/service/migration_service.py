from service.custom_multipart_upload import Status
from service.glacier_service import GlacierService
from service.s3_service import S3Service


class MigrationService:
    def __init__(self, key):
        self._s3_service = S3Service()
        self._glacier_service = GlacierService()
        self._s3_service.init_upload(key)

    def migrate(self, job_id, arch_size):
        chunk_generator = self._glacier_service.chunk_generator(job_id, arch_size)

        for chunk in chunk_generator:
            self._s3_service.upload_chunk(chunk.get('body'))

        if self._s3_service.get_status() == Status.ACTIVE:
            self._s3_service.finish()

        return job_id
