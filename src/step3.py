import concurrent
import logging
from concurrent.futures.thread import ThreadPoolExecutor

from config.config import UPLOAD_THREADS
from config.log_conf import initialize_logging
from service.migration_service import MigrationService


def migrate():
    with open(f'output_step2/input_jobs', encoding='utf-8') as input_file:
        list_jobs = input_file.readlines()

    with open(f'output_step3/completed_jobs', "w", encoding='utf-8') as output_file:
        with ThreadPoolExecutor(max_workers=UPLOAD_THREADS) as executor:
            futures = []
            for job in list_jobs:
                job_id, arch_path, arch_size = job.split('|||')
                migration_service = MigrationService()
                futures.append(executor.submit(migration_service.migrate, job_id=job_id, key=arch_path, size=int(arch_size)))

            for future in concurrent.futures.as_completed(futures):
                try:
                    output_file.write(future.result() + '\n')
                except Exception as e:
                    logging.error(e)


if __name__ == '__main__':
    initialize_logging()
    migrate()
