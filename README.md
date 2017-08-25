# AWS Mobile Analytics to Elasticsearch & Kibana
Import AWS Mobile Analytics data into Elasticsearch to view and analyze within Kibana.

### Requirements
- Docker with docker-compose
- Python and requests library
    - `pip install requests`

### Running

1. Start Docker containers for Elasticsearch and Kibana. Starting Kibana can take a while - I've seen it take 5 min on MacBook Pro.
```
docker-compose up
```

2. Run the Python import script (example with all the arguments)
```
python import.py \
    --name "ColorPal" \
    --aws-profile default \
    --bucket mobile-analytics-.../awsma/events/{app-id}} \
    --year 2017 \
    --month 7 \
    --day 29 \
    --delete-date 2017-07-29 \
    --no-s3-import
```


### Import Arguments
| Arguments&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Description |
| --- | --- |
| --bucket | **Required** AWS Mobile Analytics S3 bucket - full path up to the year<br>Example: `mobile-analytics-.../awsma/events/be2b019...`
| --name   | Elasticsearch index name - defaults to `app`. The full index name will be prepended with "awsma_" to use the index mapping template. Also, spaces will be removed and characters will be forced to lowercase.
| --aws-profile | AWS CLI profile name. Will use the `default` profile name if not set
| --year   | Year to import
| --month  | Month to import - **must also include --year**
| --day    | Day to import - **must also include --year & --month**
| --delete-date | Delete a certain date or date range. Months or days with a single digits must have a leading zero. (`8` should be `08`) Single date: `2017-08-01` Or all of a month `2017-08-*`
| --no-s3-import | Flag to **not** import files from S3. Useful if you already have the files downloaded

## What's Going On in the Python Import
1. Downloads the AWS Mobile Analytics S3 files locally
2. Unzips the S3 gzipped files
3. Creates custom mapping if one does not already exist
4. Create Elasticsearch index by date
4. Import unzipped S3 files into Elasticsearch
