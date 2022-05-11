import os, boto3, json, requests
from datetime import datetime
from flask import Flask, jsonify, make_response, request
from pkg import session
from pkg.models import Campaigns, Advertible, Events
from pkg.klavijo import Klavijo
from boto3.dynamodb.types import TypeSerializer

app = Flask(__name__)
dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )

#"KLAVIJO_CAMPAIGNS = os.environ['KLAVIJO_CAMPAIGNS']

# PREGUNTO POR LAS CAMPAÑAS EN KLAVIJO Y LA CARGO COMO ADVERTISABLE
def get_advertible():
    klavijo_campaigns = Klavijo()
    campaigns = klavijo_campaigns.get_objects(object="campaigns", count=25000, sort=None, type=0)
    for campaign in campaigns[0]:
        print(campaign.get('id'), campaign.get('name'))
        q = session.query(Advertible).filter(Advertible.adroll_id == campaign.get('id')).first()
        if q:
            print("Campaign already exists")
        else:
            print(f"Campaign {campaign.get('name')} not found, CREANDO")
            new_campaign = Advertible(adroll_id=campaign.get('id'), name=campaign.get('name'), supplier_id=11, type_add='Klavijo', status=1, organization_id=3)
            session.add(new_campaign)
            session.commit()

# Ir a buscar un advertible del tipo Klavijo y verificar si existe como campaigns
def get_campaigns():
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

def get_events():
    a=Klavijo()
    b=a.get_objects(object="metrics", count=5, sort=None, type=0)
    for metrics in b:
        for metric in metrics:
            d = Klavijo()
            e = d.get_objects(object="metric", count=100, sort=None, type=1, object_id=metric.get('id'), element_name="timeline")
            c = 0
            for line in e:
                for row in line:
                    print("-----------------------------------------------------")
                    print(row.get('id'), metric.get('id'))
                    print(row)
                    q = session.query(Events).filter(Events.provider_id == row.get('id')).first()
                    if q:
                        print("Event already exists")
                    else:
                        event_properties = row.get('event_properties')
                        campaign_name = event_properties.get('Campaign Name')
                        print(campaign_name)
                        campaign = session.query(Advertible).filter(Advertible.name == campaign_name).first()
                        print({'campaign': campaign})
                        try:
                            event = Events(provider_id=row.get('id'), advertisable_id=campaign.id)
                            session.add(event)
                            session.commit()
                        except Exception as e:
                            print(e)
                    # campaign_dict.update({'date': datetime.now().strftime("%Y-%m-%d"), 'campaignId': str(campaign.provider_id)})
                    # serializer = TypeSerializer()
                    # low_level_copy = {k: serializer.serialize(v) for k,v in campaign_dict.items()}

#get_events()

def get_campaign_recipients():
    # VOY A TOMAR TODAS LAS CAMPAÑAS (EN KLAVIJO UNA CAMPAÑA ES UN ADVERTIBLE, PARA PODER ASOCIAR LA CAMPAÑA/ADVERTIBLE A UNA ORGANIZACION)
    campaign = session.query(Advertible).filter(Advertible.supplier_id==11).all()
    if campaign:
        for line in campaign:
            klavijo_client = Klavijo()

            e = klavijo_client.get_objects(object="campaign", object_id=line.adroll_id, element_name="recipients",count=25000, sort=None, type=1)
            for line1 in e:
                for q in line1:
                    print(q.get('status'), q.get('customer_id'), q.get('email'), line.adroll_id, line.id)

# get_campaign_recipients()