import base64
import json
import logging
import re
from json.decoder import JSONDecodeError

from src.config.config import SPLIT_SIZE, INVENTORY_JSON
from src.config.log_conf import initialize_logging


def split_list(file_name):
    with open(f'input_step1/%s' % file_name, encoding='utf-8') as input_file:
        list_json = json.load(input_file).get('ArchiveList')

    list_json_chunks = [list_json[i:i + SPLIT_SIZE] for i in range(0, len(list_json), SPLIT_SIZE)]

    prep_id = 1
    for chunk in list_json_chunks:
        with open(f'output_step1/input_split_%s' % prep_id, "w", encoding='utf-8') as output_file:
            for job in chunk:
                try:
                    arch_id = job.get('ArchiveId')
                    arch_size = job.get('Size')
                    arch_path = json.loads(job.get('ArchiveDescription')).get('path')
                except JSONDecodeError as je:
                    arch_path = base64.b64decode(re.compile('<p>(.*?)</p>').search(job.get('ArchiveDescription')).group(1))
                    logging.info(arch_path)
                except Exception as e:
                    logging.error(e)
                    logging.error(job)
                    raise e

                output_file.write('%s|||%s|||%s' % (arch_id, arch_path, arch_size))
                output_file.write('\n')
        prep_id = prep_id + 1


if __name__ == '__main__':
    initialize_logging()
    split_list(INVENTORY_JSON)