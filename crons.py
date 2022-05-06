import os, boto3, json, requests, datetime
from flask import Flask, jsonify, make_response, request
from pkg.models import Campaigns
from pkg.klavijo import Klavijo
from boto3.dynamodb.types import TypeSerializer

app = Flask(__name__)
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )

# USERS_TABLE = os.environ['USERS_TABLE']
# KLAVIJO = os.environ['KLAVIJO']

def get_campaigns(user_id):
    klavijo_campaigns = Klavijo()
    data = klavijo_campaigns.get_campaigns()
    for line in data:
        for campaign in line:
            campaign.update({'date': datetime.now().strftime("%Y-%m-%d"), 'advertisableId': str(q.id)})
            serializer = TypeSerializer()
            low_level_copy = {k: serializer.serialize(v) for k,v in body.items()}
            print(low_level_copy)
            dynamodb_client.put_item(TableName=REPORTS_TABLE, Item=low_level_copy)


    # result = dynamodb_client.get_item(
    #     TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    # )
    # item = result.get('Item')
    # if not item:
    #     return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    # return jsonify(
    #     {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    # )

get_campaigns(1)