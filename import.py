import argparse, os, requests, sys, subprocess, shutil, time, json
from datetime import datetime

parser = argparse.ArgumentParser(description='Export AWS Mobile Analytics from S3 to Local Elasticsearch Docker container')
parser.add_argument('--bucket',  required=True, help='AWS Mobile Analytics full S3 bucket path up to year')
parser.add_argument('--name',  help='Elasticsearch index name [app]', type=str, default='app')
parser.add_argument('--aws-profile',  help='AWS CLI profile name [default]', default='default')
parser.add_argument('--year',  type=lambda y: datetime.strptime(y, '%Y'), help='S3 year bucket')
parser.add_argument('--month', type=lambda m: datetime.strptime(m, '%m'), help='S3 month bucket')
parser.add_argument('--day',   type=lambda d: datetime.strptime(d, '%d'), help='S3 day bucket')
parser.add_argument('--delete-date',  help='Elasticsearch date to delete', type=str)
parser.add_argument('--no-s3-import',  help='Do not import files from S3', dest='no_s3_import', action='store_true')
args = parser.parse_args()

# Create temp directory for S3 files (remove if exists)
temp_save_path = os.getcwd()+'/_temp'
if args.no_s3_import != True:
    if os.path.exists(temp_save_path):
        shutil.rmtree(temp_save_path+'/')

    os.makedirs(temp_save_path)

    # Create S3 path
    year = month = day = ''
    if args.year: year = args.year.strftime('%Y')
    if args.month: month = args.month.strftime('%m')
    if args.day: day = args.day.strftime('%d')
    s3_path = os.path.join(args.bucket,year,month,day)

    print 'Importing S3 files...'
    subprocess.check_output('aws s3 cp s3://'+s3_path+' '+temp_save_path+' --recursive --profile '+args.aws_profile, shell=True)

    print 'Unzipping S3 files...'
    subprocess.check_output('gunzip -rf '+temp_save_path+'/*', shell=True)

print 'Importing files into Elasticsearch...'
esIndex = "awsma_%s" % str(args.name).lower().replace(" ", "")
esType = "logs"

with open('./config/mapping.json', 'r') as es_mapping:
    mapping=es_mapping.read()

# Name of Elasticsearch index to delete
if args.delete_date:
    requests.delete("http://0.0.0.0:9200/"+esIndex+"-"+args.delete_date)

# Add index mapping
requests.post("http://0.0.0.0:9200/_template/"+esIndex, data=mapping)

# Loop over S3 files and export to Elasticsearch
for path, subdirs, files in os.walk(temp_save_path):
    for name in files:
        with open(os.path.join(path, name), 'r') as myfile:
            for line in myfile:
                jsonObj = json.loads(line)
                timestamp = jsonObj['session']['start_timestamp'] / 1000
                index_postfix = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

                headers = {'Content-Type': 'application/json', 'Content-Length': str(len(line)) }
                r = requests.post("http://0.0.0.0:9200/"+esIndex+"-"+index_postfix+"/"+esType, data=line, headers=headers)

                if r.status_code != 201:
                    print "Unable to load "+os.path.join(path, name)+" "+str(r.status_code)+" "+r.body.reason


print "-----------------------------------------"
print "Kibana index pattern: %s*" % esIndex
print "-----------------------------------------"
