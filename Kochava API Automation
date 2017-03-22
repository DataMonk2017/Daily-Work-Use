# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:03:55 2016

@author: Jeremy
"""

import pandas as pd 
import json
import time
import datetime
import requests
import os

from multiprocessing.dummy import Pool as ThreadPool
from datetime import timedelta
#%%
path=r'C:\Users\jeremy\Desktop\HMH Daily Export'
os.chdir(path+'\\GMG\\event')
subdirectory =(datetime.date.today()).strftime('%m-%d-%Y') #"download_%s"%('click_mobilda')
try:
    os.mkdir(subdirectory)
except Exception:
    pass

new_path=path+'\\GMG\\event\\'+subdirectory
time_interval=15
event_name=['Bundle Purchasek-2',"Grade 1 Purchase","Grade 2 Purchase","Grade K Purchase"]
app_guid="kogo-math-go----ios----prod56fd9d987becc"
#%%
def get_event(test_list):
    app_guid=test_list[0]
    start_time=test_list[1]
    end_time=test_list[2]
    event_name=test_list[3]
    app_name=test_list[4]
    pattern = '%d.%m.%Y %H:%M:%S'
    start_epoch = str(int((datetime.datetime.strptime(start_time,pattern) - datetime.datetime.strptime("1970-1-1","%Y-%m-%d")).total_seconds()))

    #start_epoch = str(int(time.mktime(time.strptime(start_time, pattern))))
    #print(start_epoch)
    end_epoch = str(int((datetime.datetime.strptime(end_time,pattern) - datetime.datetime.strptime("1970-1-1","%Y-%m-%d")).total_seconds()))
    #end_epoch = str(int(time.mktime(time.strptime(end_time, pattern))))   
    headers = {'content-type': 'application/json'}
    
    post_data2={
      "api_key": "E0663704-485B-479A-8448-C169A92D714F",
      "app_guid": app_guid,
      "time_start": start_epoch,
      "time_end":end_epoch ,
      "traffic": [
        "event"
      ],
      "traffic_filtering":{
      "event_name":event_name
      },
      "traffic_including":["unattributed_traffic"],    
    "delivery_method": [
        "S3link"
      ],
      "time_zone": "US/Pacific",
      "delivery_format": "csv",
      "columns_order":[
      "timestamp_utc",
      "timestamp_adjusted",
      "event_name",
      "event_time_registered",
      "geo_country",
      "geo_region",
      "geo_city",
      "device_type",
      "device_os",
      "device_version",
      "device_id_adid",
      "device_id_android_id",
      "device_id_kochava",
      "device_id_idfv",
      "device_id_idfa",
      "device_id_custom",
      "request_ua",
      "request_ip",
      "attribution_attribution_action",
      "attribution_timestamp",
      "attribution_timestamp_adjusted",
      "attribution_matched_by",
      "attribution_matched_to",
      "attribution_network_id",
      "attribution_network",
      "attribution_campaign_id",
      "attribution_campaign",
      "attribution_tier",
      "attribution_tracker_id",
      "attribution_tracker",
      "attribution_site_id",
      "attribution_creative",
      "attribution_date_utc",
      "attribution_date_adjusted",
      "attribution_seconds_since",
      "custom_dimensions",
      "dimension_data",
      "dimension_count",
      "dimension_sum",
      "count",
      "install_matched_on",
      "install_status",
      "install_date_utc",
      "install_date_adjusted",
      "install_matched_by",
      "install_device_version",
      "install_devices_idfa",
      "install_devices_android_id",
      "install_devices_adid",'click_original_request']  
    }

    post_data2=json.dumps(post_data2)
    post_response2 =requests.post(url='https://reporting.api.kochava.com/v1.1/detail',data=post_data2, headers=headers)
    string2=post_response2.content.decode('utf-8')
    json_obj2 = json.loads(string2)
    report_token2=json_obj2['report_token']
    data2={
        "api_key": "E0663704-485B-479A-8448-C169A92D714F",
        "app_guid": app_guid,
        "token": report_token2,
    }
    data2=json.dumps(data2)
    
    url_json2 = dict()
    url_json2['progress']='0'
    #Set the system to sleep while waiting for response
    while url_json2['progress']!='100':
        time.sleep(30)
        report_status =requests.post(url='https://reporting.api.kochava.com/v1.1/progress',data=data2, headers=headers)
        urlstring=report_status.content.decode('utf-8')
        url_json2 = json.loads(urlstring) 
    
    url2=url_json2['report']
    eventraw= pd.io.parsers.read_csv(url2)
    eventraw.to_csv(new_path+'\\%s_event.csv'%app_name,index=False)
    return eventraw      
#%%
def split_timeinterval(app_guid,start_date, end_date, interval, event_name):
    """
    If the optional hourly interval is provided in config.json, then this function will generate 
    jobs for those intervals beginning at the start_date.
    """
    start_date=datetime.datetime.strptime(start_date,'%d.%m.%Y %H:%M:%S')
    end_date=datetime.datetime.strptime(end_date,'%d.%m.%Y %H:%M:%S')
    timeline = []
    count=0
    if interval == None:
        start_date=start_date.strftime('%d.%m.%Y %H:%M:%S')
        end_date=end_date.strftime('%d.%m.%Y %H:%M:%S')
        timeline.append([app_guid,start_date,end_date,event_name,str(count)])

    else:
        end = start_date + timedelta(days=interval)
        if end > end_date:
            start_date1=start_date.strftime('%d.%m.%Y %H:%M:%S')
            end_date1=end_date.strftime('%d.%m.%Y %H:%M:%S')
            timeline.append([app_guid,start_date1,end_date1,event_name,str(count)])
        else:
            start = start_date
            while end < end_date:
                start1=start.strftime('%d.%m.%Y %H:%M:%S')
                end1=end.strftime('%d.%m.%Y %H:%M:%S')
                timeline.append([app_guid,start1,end1,event_name,str(count)])
                start = end
                end = start + timedelta(days=interval)
                count+=1
            start1=start.strftime('%d.%m.%Y %H:%M:%S')    
            end_date1=end_date.strftime('%d.%m.%Y %H:%M:%S')
            timeline.append([app_guid,start1,end_date1,event_name,str(count)])
    return timeline    

    
#%%

#monday_date=(datetime.date.today()- datetime.timedelta(datetime.date.today().weekday())).strftime('%b-%d-%Y')
#facebook_df = pd.read_csv('Curious-World-All-Ads-Aug-17-2016-_-%s.csv'%facebook_Date)
start_time = '07.10.2016 00:00:00' 
end_time = (datetime.date.today()).strftime('%d.%m.%Y %H:%M:%S')#'26.10.2016 00:00:00'#datetime.date.today().strftime('%d.%m.%Y %H:%M:%S')

#start_time = '01.01.2016 00:00:00' 
#end_time = '06.10.2016 00:00:00'

#%%

e_list=tuple(split_timeinterval(app_guid,start_time,end_time,time_interval,event_name))

start = time.time()
pool = ThreadPool(len(e_list))
pool.map(get_event, e_list)    
print('Test:', time.time() - start)
#%%
if os.path.isfile(path+'\\gmg_event%s.csv'%((datetime.date.today()).strftime('%m-%d-%Y'))):
    os.remove(path+'\\gmg_event%s.csv'%((datetime.date.today()).strftime('%m-%d-%Y')))
list_csv=[new_path+"\\"+file for file in os.listdir(new_path) if ".csv" in file]
chunksize = 10**6
count=0
for f in list_csv:
    for chunk in pd.read_csv(f, chunksize=chunksize,encoding="ISO8859-1",dtype=str):
        chunk.to_csv(path+'\\gmg_event%s.csv'%((datetime.date.today()).strftime('%m-%d-%Y')),mode='a',index=False )
        count+=chunk.shape[0]
