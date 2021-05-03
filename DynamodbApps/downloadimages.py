import requests
import boto3

#reference dynamodb
dynamodb = boto3.resource('dynamodb')
#point at music table
table = dynamodb.Table('Music')
#get image url values from dynamodb
ScanResponse = table.scan(AttributesToGet=['img_url'])


#download all images from their urls
for record in ScanResponse['Items']:
    img_url = record['img_url']
    file_name = img_url.split('/')[-1]
    response = requests.get(img_url)
    with open("/Users/abdotech/Desktop/images/"+file_name, "wb") as file:
      for chunk in response:
        file.write(chunk)


    file.close()    