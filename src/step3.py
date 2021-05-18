import concurrent
import logging
import gc
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import FIRST_COMPLETED

from config.config import UPLOAD_THREADS
from config.log_conf import initialize_logging
from service.migration_service import MigrationService


def migrate():
    with open(f'output_step2/input_jobs', encoding='utf-8') as input_file:
        list_jobs = input_file.readlines()

    with open(f'output_step3/completed_jobs', "w", encoding='utf-8') as output_file:
        with open(f'output_step3/errors', "w", encoding='utf-8') as errors_file:
            with ThreadPoolExecutor(max_workers=UPLOAD_THREADS) as executor:
                futures = []
                while list_jobs or futures:
                    # add theads up to target value
                    while list_jobs and len(futures) < UPLOAD_THREADS:
                        job = list_jobs.pop(0)
                        job_id, arch_path, arch_size = job.split('|||')
                        migration_service = MigrationService()
                        futures.append(executor.submit(migration_service.migrate, job_id=job_id, key=arch_path, size=int(arch_size)))

                    # wait of at least on thread to complete
                    finished, unfinished = concurrent.futures.wait(futures, timeout=None, return_when=FIRST_COMPLETED)
                    logging.debug('FINISHED %s future(s)', len(finished))
                    for future in finished:
                        try:
                            result = future.result()
                            logging.info('DONE job %s' % result)
                            output_file.write(result + '\n')
                            output_file.flush()
                            logging.info('SAVED job %s' % result)
                        except Exception as e:
                            logging.error(e)
                            errors_file.write('EXCEPTION: %s\n' % (e))
                            errors_file.flush()
                        futures.remove(future)

                    # clean up memory
                    del finished
                    logging.debug('Collected %s', gc.collect())
                logging.info('ALL DONE.')

if __name__ == '__main__':
    initialize_logging()
    migrate()
