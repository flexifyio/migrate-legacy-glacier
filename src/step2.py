import logging

from src.config.config import PROCESSING_SPLIT
from src.config.log_conf import initialize_logging
from src.service.glacier_service import GlacierService


def init_jobs(file_name):
    with open(f'output_step1/%s' % file_name, encoding='utf-8') as input_file:
        archs = input_file.readlines()

    job_ids = []
    service = GlacierService()

    for arch in archs:
        arc_name, arch_path, arch_size = arch.split(' ')
        job_ids.append('%s %s %s' % (service.create_jobs(arc_name).get('jobId'), arch_path, arch_size))
        logging.info("initiated for %s" % arch)

    with open(f'output_step2/input_jobs', "w", encoding='utf-8') as output_file:
        for job in job_ids:
            output_file.write(job)


if __name__ == '__main__':
    initialize_logging()
    init_jobs(PROCESSING_SPLIT)
