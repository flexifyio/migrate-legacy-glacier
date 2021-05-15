from client.glacier_client import GlacierClient
from config.config import GL_VAULT, CHUNK_SIZE, GL_TIER


class GlacierService:
    def __init__(self):
        self._client = GlacierClient().get_client()
        self._vault = GL_VAULT

    def create_jobs(self, arch_id, arch_path):
        return self._client.initiate_job(
            vaultName=self._vault,
            jobParameters={
                'Type': 'archive-retrieval',
                'ArchiveId': arch_id,
                'Description': 'Restore by Flexify',
                'Tier:': GL_TIER})

    def fetch_jobs(self):
        pass

    def chunk_generator(self, job_id, arch_size):
        start = 0
        while True:
            end = arch_size - 1 if start + CHUNK_SIZE > arch_size else start + CHUNK_SIZE
            yield self._client.get_job_output(vaultName=self._vault, jobId=job_id, range='bytes={}-{}'.format(start, end))
            start = end + 1

            if end == arch_size - 1:
                break
