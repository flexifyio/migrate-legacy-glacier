import base64
import json
import logging
import re
from json.decoder import JSONDecodeError

from config.config import SPLIT_SIZE, SPLIT_COUNT, INVENTORY_JSON, DESCRIPTION_FORMAT
from config.log_conf import initialize_logging


def split_list(file_name):
    with open(f'input_step1/%s' % file_name, encoding='utf-8') as input_file:
        list_json = json.load(input_file).get('ArchiveList')

        total_size=0
        total_count=0
        chunk_id = 1
        chunk_start = 0
        while chunk_start < len(list_json):
            chunk_size = 0
            chunk_count = 0
            with open(f'output_step1/split_%02d' % chunk_id, "w", encoding='utf-8') as output_file:
                for i in range(chunk_start, len(list_json)):
                    job = list_json[i]
                    try:
                        arch_id = job.get('ArchiveId')
                        arch_size = job.get('Size')
                        arc_description = job.get('ArchiveDescription')
                        if DESCRIPTION_FORMAT == 'PATH':
                            arch_path = arc_description
                        elif DESCRIPTION_FORMAT == 'JSON':
                            try:
                                arch_path = json.loads(arc_description).get('path')
                            except JSONDecodeError as je:
                                enc_arch_path = base64.b64decode(re.compile('<p>(.*?)</p>').search(arc_description).group(1))
                                arch_path = enc_arch_path.decode()
                        else:
                            raise ValueError('Unknown value of DESCRIPTION_FORMAT. Check configuration')
                        # logging.debug(arch_path)
                    except Exception as e:
                        logging.error(e)
                        logging.error(job)
                        raise e

                    if arch_path is None:
                        logging.warning('None arch_path for %s', arch_id)
                        continue

                    output_file.write('%s|||%s|||%s' % (arch_id, arch_path, arch_size))
                    output_file.write('\n')
                    chunk_size = chunk_size + arch_size
                    chunk_count = chunk_count + 1

                    chunk_start = i + 1
                    if (chunk_size >= SPLIT_SIZE or chunk_count >= SPLIT_COUNT):
                        break

            logging.info("part %s: %d objects %.2f GB (%d bytes)", chunk_id, chunk_count, chunk_size/1024./1024./1024., chunk_size)
            total_size = total_size + chunk_size
            total_count = total_count + chunk_count
            chunk_id = chunk_id + 1

        logging.info("---------")
        logging.info("TOTAL: %d objects %.2f GB (%d bytes)", total_count, total_size/1024./1024./1024., total_size)

if __name__ == '__main__':
    initialize_logging()
    split_list(INVENTORY_JSON)
