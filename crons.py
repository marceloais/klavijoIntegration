import os, boto3, json, requests, datetime
from flask import Flask, jsonify, make_response, request
from pkg import session
from pkg.models import Campaigns, Advertible
from pkg.klavijo import Klavijo
from boto3.dynamodb.types import TypeSerializer

app = Flask(__name__)
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )

KLAVIJO_CAMPAIGNS = os.environ['KLAVIJO_CAMPAIGNS']


# Ir a buscar un advertible del tipo Klavijo y verificar si existe
def get_advertible(advertiser_id):
    advertiser = session.query(Advertible).filter(Advertible.supplier_id==11).all()
    if advertiser:
        for line in advertiser:
            print(line.adroll_id, line.supplier_id, line.name)
            q = session.query(Campaigns).filter(Campaigns.provider_id == line.adroll_id).first()
            if not q:
                new_campaign = Campaigns(provider_id=line.adroll_id, advertisable_id=line.id)
                session.add(new_campaign)
                session.commit()
                print(new_campaign.__dict__)
            else:
                print({'success': 'Campaign found'})

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
