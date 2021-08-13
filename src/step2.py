import logging

from config.config import PROCESSING_SPLIT
from config.log_conf import initialize_logging
from service.glacier_service import GlacierService


def init_jobs(split_num):
    file_name = f'output_step2/jobs_%02d' % split_num
    skip_size = 0

    try:
        with open(file_name) as input_jobs:
            skip_size = len(input_jobs.readlines())
    except IOError:
        logging.info(f'Output file %s was not created yet' % file_name)

    with open(f'output_step1/split_%02d' % split_num, encoding='utf-8') as input_file:
        logging.info(f'Skipping first %d lines' % skip_size)
        archives = input_file.readlines()[skip_size:]

    service = GlacierService()

    with open(file_name, "w", encoding='utf-8') as output_file:
        for arch in archives:
            arc_id, arch_path, arch_size = arch.split('|||')
            output_file.write('%s|||%s|||%s' % (service.create_jobs(arc_id).get('jobId'), arch_path, arch_size))
            output_file.flush()
            logging.info("Job initiated for %s" % arch)


if __name__ == '__main__':
    initialize_logging()
    init_jobs(PROCESSING_SPLIT)
