## Step 0: Get inventory from Amazon Glacier
```sh
aws glacier initiate-job --account-id - --vault-name <vault> --job-parameters '{"Type": "inventory-retrieval"}'
aws glacier describe-job --account-id - --vault-name <vault> --job-id '<job-id>'
aws glacier get-job-output  --account-id - --vault-name <vault> --job-id '<job-id>' inventory.json
```

## Step 1: Split inventory file
1. Put `inventory.json` to `input_step1` directory
2. Edit `src/config/config.py` and set `INVENTORY_JSON` to the name of the inventory file
3. Run `python3 src/step1.py`
4. See parts inside `output_step1`

# Step 2: Run Glacier restore jobs
1. Set `PROCESSING_SPLIT` in `src/config/config.py` to the part you'd like to process
2. Configure Glacier properties in `src/config/config.py`
3. Run `python3 src/step2.py`
4. Glacier job IDs will be saved to `output_step2`

*Wait for jobs to complete*

# Step: Copy restored archives to S3
1. Make sure jobs complete
2. Configure S3 options in `src/config/config.py`
3. Rub copy with `python3 src/step3.py`
