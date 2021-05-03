from decimal import Decimal
import json
import boto3

#load movies
def load_songs(songs,dynamodb=None):

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Music')
    for music in songs['songs']:
        title = music['title']
        artists = music['artist']
        print("Adding songs:",title,artists)
        table.put_item(Item=music)




if __name__ == '__main__':
    with open("/Users/abdotech/Desktop/cc-ass2-MusicApp/a2.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
    load_songs(music_list)   