# size of inventory file split in bytes
# about 3.5 TiB can be processed in 12 hours
SPLIT_SIZE = 3 * 1024 * 1024 * 1024 * 1024

# size of inventory split in the number of files
SPLIT_COUNT =  10000

# inventory file name in /src/input_step1 e.g. 'inventory.json'
INVENTORY_JSON = 'inventory.json'

# how to extract object name from ArchiveDescription (PATH or JSON)
DESCRIPTION_FORMAT='PATH'

# split number to process on step 2 and step 3
PROCESSING_SPLIT = 1

UPLOAD_THREADS = 64

# size of a chunk downloaded from vault (6 MiB)
CHUNK_SIZE = 64 * 1024 * 1024

# glacier
GL_KEY = ''
GL_SECRET = ''
GL_VAULT = ''
GL_REGION = ''
GL_TIER = 'Bulk'

# s3
S3_KEY = ''
S3_SECRET = ''
S3_BUCKET = ''
S3_REGION = 'us-east-1'
