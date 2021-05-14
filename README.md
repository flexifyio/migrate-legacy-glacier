## Step 0: Get inventory from Amazon Glacier
```sh
aws glacier initiate-job --account-id - --region us-east-1 --profile glacier --vault-name flexify-glacier --job-parameters '{"Type": "inventory-retrieval"}'
aws glacier describe-job --account-id - --region us-east-1 --profile glacier --vault-name flexify-glacier --job-id '…..'
aws glacier get-job-output  --account-id - --region us-east-1 --profile glacier --vault-name flexify-glacier --job-id '…' output.json
```

## Step 1: Split inventory file

1. Put `inventory.json` to `input_step1` directory
2. Edit `src/config/config.py` and set `INVENTORY_JSON` and `PROCESSING_SPLIT` properties
3. Create directory `output_step1`
4. Run `python3 src/step1.py`
5. See parts inside `output_step1`