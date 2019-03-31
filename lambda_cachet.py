from botocore.vendored import requests
import datetime
from dateutil.tz import tzoffset

# UCLAPI key to use for test requests
token = "uclapi-PUT_TOKEN_HERE"
# Set cachet API key and we don't use a json body
payload_headers = {"X-Cachet-Token":"TOKEN_HERE", "Content-Type": "application/x-www-form-urlencoded"}
# Get current time
now = datetime.datetime.now(tzoffset('GMT', 0))
time_total = []

def update_cachet_endpoint(url,id,expiry_time,extra_params=None):
    params = {"token":token}
    if extra_params:
        params.update(extra_params)
    r = requests.get(url,params=params)
    stamp = r.headers["Last-Modified"]
    date = datetime.datetime.strptime(stamp, '%a, %d %b %Y %X %Z')
    date = date.replace(tzinfo=tzoffset('GMT',0))
    minutes = int((now - date).total_seconds() / 60)
    time_total.append(r.elapsed.total_seconds()*1000)
    if minutes > expiry_time:
        status = 4
        url = "https://cachet.apps.uclapi.com/api/v1/components/"
        requests.put(url+str(id),data={"status":status},headers=payload_headers)

def update_cachet_url_ping(url,id):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        status = 1
    else:
        status = 4
    url = "https://cachet.apps.uclapi.com/api/v1/components/"
    requests.put(url+str(id),data={"status":status},headers=payload_headers)

def update_cachet_metric(value,id):
    url = "https://cachet.apps.uclapi.com/api/v1/metrics/"+str(id)+"/points/"
    requests.post(url,data={"value":value},headers=payload_headers)

def my_handler(event, context):
    #token = event['uclapi_token']
    #payload_headers["X-Cachet-Token"] = event['cachet_token']
    url = "https://uclapi.com/"
    update_cachet_endpoint(url+"workspaces/surveys",3,15)
    update_cachet_endpoint(url+"timetable/data/departments",2,45)
    update_cachet_url_ping(url,4)
    sum = 0
    count = 0
    for time in time_total:
        sum += time
        count += 1
    average_request_time = sum/count
    update_cachet_metric(average_request_time,1)
