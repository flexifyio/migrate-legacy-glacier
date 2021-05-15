# size of inventory file split
SPLIT_SIZE = 100000

# inventory file name in /src/input_step1 e.g. 'inventory.json'
INVENTORY_JSON = ''

# inventory split file name in /src/output_step1 e.g. 'input_split_1'
PROCESSING_SPLIT = ''

UPLOAD_THREADS = 5

# size of a chunk downloaded from vault (6 mb)
CHUNK_SIZE = 6 * 1024 * 1024

# glacier
GL_KEY = 'AKIAVHCLHRT4DJF652NK'
GL_SECRET = 'Lxw2JaAXJ2wyBj1Q2AlSrJFWuwmzyfSUpBsidBYQ'
GL_VAULT = 'flexify-glacier'
GL_REGION = 'us-east-1'
GL_TIER = 'Bulk'

# s3
S3_KEY = 'AKIAIVW6TZW6Q4MBZZ7A'
S3_SECRET = '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'
S3_BUCKET = 'flexify'
S3_REGION = 'us-east-1'
