import logging
import boto3
import os

from botocore.exceptions import ClientError

s3_client= boto3.client('s3')

#uplaod files
def upload_file(file_name,bucket,object_name=None):

    for root,dirs,files in os.walk(file_name):
        for file in files:
            s3_client.upload_file(os.path.join(root,file),bucket,file)
    return True


#operations
print(upload_file('/Users/abdotech/Desktop/images','musicimages6969'))   