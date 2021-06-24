import base64
import json
import logging
import re
from json.decoder import JSONDecodeError

from config.config import SPLIT_SIZE, INVENTORY_JSON, DESCRIPTION_FORMAT
from config.log_conf import initialize_logging


def split_list(file_name):
    with open(f'input_step1/%s' % file_name, encoding='utf-8') as input_file:
        list_json = json.load(input_file).get('ArchiveList')

    list_json_chunks = [list_json[i:i + SPLIT_SIZE] for i in range(0, len(list_json), SPLIT_SIZE)]

    prep_id = 1
    for chunk in list_json_chunks:
        total_size=0
        with open(f'output_step1/input_split_%s' % prep_id, "w", encoding='utf-8') as output_file:
            for job in chunk:
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
                    # logging.info(arch_path)
                except Exception as e:
                    logging.error(e)
                    logging.error(job)
                    raise e

                if arch_path is None:
                    logging.warning('None arch_path for %s', arch_id)
                    continue

                output_file.write('%s|||%s|||%s' % (arch_id, arch_path, arch_size))
                output_file.write('\n')
                total_size = total_size + arch_size
        logging.info("part %s size %.2f GB (%d bytes)", prep_id, total_size/1024./1024./1024., total_size)
        prep_id = prep_id + 1


if __name__ == '__main__':
    initialize_logging()
    split_list(INVENTORY_JSON)