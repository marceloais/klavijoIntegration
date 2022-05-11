from turtle import pos
import requests, json

from pkg.models import Campaigns

class Klavijo:
    
    def __init__(self):
        self.api_key = "pk_62eddd6e696c0f55657837f33ec7ee3c8c"
        self.url = str()
        self.headers = {"Accept": "application/json"}
        self.metrics = dict()
    
    def create_url(self, object=None, page=None, count=None, sort=None):
        url = f"https://a.klaviyo.com/api/v1/"
        if object:
            url += f"{object}?"
        if page or page==0:
            url += f"&page={page}"
        if count:
            url += f"&count={count}"
        if sort:
            url += f"&sort={sort}"
        if self.api_key:
            url += f"&api_key={self.api_key}"
        self.url = url
        return url
    
    def get_campaigns(self):
        positive, data_list = True, list()
        c = 0
        
        while positive:
            url = self.create_url(object="campaigns", page=c, count=5)
            metrics = json.loads(requests.get(url, headers=self.headers).text)
            page_size = metrics.get("page_size")
            if page_size <= 0:
                positive = False
            c+=1
            data_list.append(metrics.get('data'))
        return data_list[:-1]

    def get_campaign_info(self, campaign_id):
        url = self.create_url(object=f"campaign/{campaign_id}")
        metrics = json.loads(requests.get(url, headers=self.headers).text)
        for key, value in metrics.items():
            print(key, value)

    def get_objects(self, object=None, object_id=None, element_name=None, count=None, sort=None, type=None):
        if type == 1:
            url_object = f"{object}/{object_id}/{element_name}"
        else:
            url_object = f"{object}"
        positive, data_list = True, list()
        c = 0
        while positive:
            url = self.create_url(object=url_object, page=c, count=count)
            metrics = json.loads(requests.get(url, headers=self.headers).text)
            if type == 0:
                page_size = metrics.get("page_size")
                if page_size <= 0:
                    positive = False
                c+=1
                data_list.append(metrics.get('data'))
            elif type == 1:
                next = metrics.get('next')
                data = metrics.get('data')
                if not next:
                    positive=False
                c+=1
                data_list.append(metrics.get('data'))
        if type == 0:
            return data_list[:-1]      
        elif type == 1:
            return data_list