import logging

import urllib3


def initialize_logging():
    # initializing logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('initializing logging')
    # suppressing boto3 logging
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)