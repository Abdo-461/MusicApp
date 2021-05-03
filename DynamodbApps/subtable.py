import boto3

#create table 
def create_subscription_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName = 'Subscription',
        KeySchema=[
            {
                'AttributeName':'user_name',
                'KeyType': 'HASH' #partition key
            },
            {
                'AttributeName':'title',
                'KeyType':'RANGE'  #sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName':'user_name',
                'AttributeType':'S'
            },
            {
                'AttributeName':'title',
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
    subscription_table = create_subscription_table()
    print("Table Status:",subscription_table.table_status)   