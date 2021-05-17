import logging

from config.config import PROCESSING_SPLIT
from config.log_conf import initialize_logging
from service.glacier_service import GlacierService


def init_jobs(file_name):
    skip_size = 0

    try:
        with open(f'output_step2/input_jobs') as input_jobs:
            skip_size = len(input_jobs.readlines())
    except IOError:
        print("Output file input_jobs was not created yet")

    with open(f'output_step1/%s' % file_name, encoding='utf-8') as input_file:
        archs = input_file.readlines()[skip_size:]

    service = GlacierService()

    with open(f'output_step2/input_jobs', "w", encoding='utf-8') as output_file:
        for arch in archs:
            arc_id, arch_path, arch_size = arch.split('|||')
            output_file.write('%s|||%s|||%s' % (service.create_jobs(arc_id).get('jobId'), arch_path, arch_size))
            output_file.flush()
            logging.info("Job initiated for %s" % arch)


if __name__ == '__main__':
    initialize_logging()
    init_jobs(PROCESSING_SPLIT)
