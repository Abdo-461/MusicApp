import boto3

#create table
def create_music_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName = 'Music',
        KeySchema=[
            {
                'AttributeName':'title',
                'KeyType': 'HASH' #partition key
            },
            {
                'AttributeName':'artist',
                'KeyType':'RANGE'  #sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'title',
                'AttributeType':'S'
            },
            {
                'AttributeName':'artist',
                'AttributeType':'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits':10,
            'WriteCapacityUnits':10
        }
    )
    return table

if __name__ == '__main__':
    music_table = create_music_table()
    print("Table Status:",music_table.table_status)    
