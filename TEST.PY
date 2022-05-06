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

    def get_metrics(self):
        url = self.create_url(object="metrics", page=0, count=100)
        metrics = json.loads(requests.get(url, headers=self.headers).text).get('data')
        for metric in metrics:
            self.metrics.update({metric.get('id'): metric.get('name')})
    
    def get_metrics_timeline(self):
        url = self.create_url(object="metrics/timeline", count=100)
        response = requests.get(url, headers=self.headers).text
        response = json.loads(response)
        print(response)
    
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

a = Klavijo()
a.get_metrics()
print(a.metrics)