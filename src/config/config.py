# size of inventory file split
SPLIT_SIZE = 100000

# inventory file name in /src/input_step1 e.g. 'inventory.json'
INVENTORY_JSON = 'inventory.json'

# how to extract object name from ArchiveDescription (PATH or JSON)
DESCRIPTION_FORMAT='PATH'

# inventory split file name in /src/output_step1 e.g. 'input_split_1'
PROCESSING_SPLIT = 'input_split_1'

UPLOAD_THREADS = 64

# size of a chunk downloaded from vault (6 mb)
CHUNK_SIZE = 64 * 1024 * 1024

# glacier
GL_KEY = ''
GL_SECRET = ''
GL_VAULT = ''
GL_REGION = 'us-east-1'
GL_TIER = 'Bulk'

# s3
S3_KEY = ''
S3_SECRET = ''
S3_BUCKET = ''
S3_REGION = 'us-east-1'
