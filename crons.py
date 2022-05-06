import os, boto3, json, requests, datetime
from flask import Flask, jsonify, make_response, request
from pkg import session
from pkg.models import Campaigns
from pkg.klavijo import Klavijo
from boto3.dynamodb.types import TypeSerializer

app = Flask(__name__)
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )

KLAVIJO_CAMPAIGNS = os.environ['KLAVIJO_CAMPAIGNS']

def get_campaigns(user_id):
    klavijo_campaigns = Klavijo()
    data = klavijo_campaigns.get_campaigns()
    for line in data:
        for campaign_dict in line:
            q = session.query(Campaigns).filter(Campaigns.provider_id == campaign_dict.get('id')).first()
            if not q:
                campaign = Campaigns(provider_id=campaign.get('id'), advertisable_id=44)
                session.add(campaign)
                session.commit()
                campaign_dict.update({'date': datetime.now().strftime("%Y-%m-%d"), 'campaignId': str(campaign.provider_id)})
                serializer = TypeSerializer()
                low_level_copy = {k: serializer.serialize(v) for k,v in campaign_dict.items()}
                dynamodb_client.put_item(TableName=KLAVIJO_CAMPAIGNS, Item=low_level_copy)
            else:
                print(f"Campaign {campaign.get('id')} already exists")


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