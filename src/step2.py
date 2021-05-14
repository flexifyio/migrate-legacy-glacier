import logging

from config.config import PROCESSING_SPLIT
from config.log_conf import initialize_logging
from service.glacier_service import GlacierService


def init_jobs(file_name):
    with open(f'output_step1/%s' % file_name, encoding='utf-8') as input_file:
        archs = input_file.readlines()

    service = GlacierService()

    with open(f'output_step2/input_jobs', "w", encoding='utf-8') as output_file:
        for arch in archs:
            arc_name, arch_path, arch_size = arch.split('|||')
            job = '%s|||%s|||%s' % (service.create_jobs(arc_name, arch_path).get('jobId'), arch_path, arch_size)
            output_file.write(job)
            logging.info("initiated for %s" % arch)

if __name__ == '__main__':
    initialize_logging()
    init_jobs(PROCESSING_SPLIT)
