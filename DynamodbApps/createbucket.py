import logging
import boto3

from botocore.exceptions import ClientError

#create bucket
def create_bucket(bucket_name, region=None):

    #create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3',region_name=region)
            location = {'LocationConstraint':region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            
    except ClientError as e:
        logging.error(e)
        return False
    return True      



#operations
print(create_bucket('musicimages6969'))   