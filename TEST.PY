from venv import create
import requests, json

class Klavijo:
    
    def __init__(self):
        self.api_key = "pk_62eddd6e696c0f55657837f33ec7ee3c8c"
        self.url = str()
        self.headers = {"Accept": "application/json"}
        self.metrics = dict()
        self.url = str()
    
    def create_url(self,object=None, page=None, count=None, sort=None):
        url = f"https://a.klaviyo.com/api/v1/"
        if object:
            url += f"{object}?"
        if page or page>=0:
            url += f"page={page}"
        if count:
            url += f"&count={count}"
        if sort:
            url += f"&sort={sort}"
        if self.api_key:
            url += f"&api_key={self.api_key}"
        self.url = url
        return url

    def get_metrics(self):
        url = self.create_url(object="metrics", page=0, count=100)
        metrics = json.loads(requests.get(url, headers=self.headers).text).get('data')
        for metric in metrics:
            self.metrics.update({metric.get('id'): metric.get('name')})
    
    def get_metrics_timeline(self):
        url = self.create_url(object="metrics/timeline", count=100)
        response = requests.get(url, headers=self.headers).text
        response = json.loads(response)
    
    def get_events_by_metric(self, metric_id):
        url = self.create_url(object=f"metric/{metric_id}/timeline", count=100)
        response = requests.get(url, headers=self.headers).text
        response = json.loads(response)
        data = response.get('data')
        return data
    
    def get_profiles(self, person_id):
        url = self.create_url(object=f"person/{person_id}")
        response = requests.get(url, headers=self.headers).text
        response = json.loads(response)
        return response

    def get_profile_detail(self):
        self.get_metrics()
        for key, value in self.metrics.items():
            for line in self.get_events_by_metric(key):
                print(f"{key}*****************{value}")
                person_id = line.get('person').get('id')
                print(self.get_profiles(person_id))

    def get_objects(self, object=None, count=None, sort=None, type=None, object_id=None):
        if type == 1:
            url_object = f"{object}/{object_id}/timeline"
        else:
            url_object = f"{object}"

        positive, data_list = True, list()
        c = 0
        while positive:
            print("*****************************")
            url = self.create_url(object=url_object, page=c, count=count)
            print(url)
            metrics = json.loads(requests.get(url, headers=self.headers).text)
            print(metrics)
            if type == 0:
                page_size = metrics.get("page_size")
                if page_size <= 0:
                    positive = False
                c+=1
                data_list.append(metrics.get('data'))

            elif type == 1:
                print("----..-----")
                next = metrics.get('next')
                data = metrics.get('data')
                for line in data:
                    print(".-.-")
                    print(line)
                if not next:
                    positive=False
                c+=1
        print("-------------------------------")
        return data_list[:-1]        
    
a=Klavijo()
b=a.get_objects(object="metrics", count=5, sort=None, type=0)
for metrics in b:
    for metric in metrics:
        d = Klavijo()
        e = d.get_objects(object="metric", count=100, sort=None, type=1, object_id=metric.get('id'))
        print(e)