# AWS Mobile Analytics to Elasticsearch & Kibana
Import AWS Mobile Analytics data into Elasticsearch to view and analyze within Kibana.

### Requirements
- Docker
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
    --bucket mobile-analytics-06-27-2017-7e779f4f3e4a451a916b743bbe5d32df/awsma/events/be2b01906dbc4cfdb06f51e761b8ab76 \
    --year 2017 \
    --month 7 \
    --day 29 \
    --delete-date 2017-07-29 \
    --no-s3-import
```


### Import Script Arguments
| Argument | Example Values | Description |
|----------|----------------|-------------|
| --bucket | `mobile-analytics-.../awsma/events/be2b019...` | **Required** AWS Mobile Analytics S3 bucket - full path up to the year
| --name   | `ColorPal`         | Elasticsearch index name - defaults to `app`. The full index name will be prepended with "awsma_" to use the index mapping template. Also, spaces will be removed and characters will be forced to lowercase.
| --aws-profile | `production`  | AWS CLI profile name. Will use the `default` profile name if not set
| --year   | `2017`             | Year to import
| --month  |  `6`, `12`         | Month to import - **must also include --year**
| --day    |   `9`, `29`        | Day to import - ** must also include --year & --month**
| --delete-date | `2017-08-05`  | Delete a certain date or date range. Months or days with a single digits must have a leading zero. (`8` should be `08`) Single date: `2017-08-01` Or all of a month `2017-08-*`
| --no-s3-import |              | Flag to **not** import files from S3. Useful if you already have the files downloaded
