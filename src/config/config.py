# size of inventory file split
SPLIT_SIZE = 100000

# inventory file name in /src/input_step1 e.g. 'inventory.json'
INVENTORY_JSON = ''

# inventory split file name in /src/output_step1 e.g. 'input_split_1'
PROCESSING_SPLIT = ''

UPLOAD_THREADS = 8

# size of a chunk downloaded from vault (6 mb)
CHUNK_SIZE = 32 * 1024 * 1024

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
