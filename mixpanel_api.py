# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:56:27 2016

@author: Jeremy
"""

import requests #for sending https request
import urllib #for url encoding
import pandas as pd
import time
import os
import datetime
from datetime import timedelta

os.chdir(r'C:\Users\jeremy\Desktop\Seeso\Audience List')

try:
    import json
except ImportError:
    import simplejson as json



api_secret='API secret'

output_properties='["$email"]'

#note 1/3/2017 wired url encoding,figure out the reason later,make it functional first
#silly sample url get from web browser
#request_url2 = 'https://mixpanel.com/api/2.0/engage?selector=(behaviors%5B%22behavior_116%22%5D+%3D%3D+0+and+behaviors%5B%22behavior_117%22%5D+%3E+10)&sort_key=properties%5B%22%24last_seen%22%5D&sort_order=descending&output_properties=%5B%22%24first_name%22%2C+%22first_name%22%2C+%22%24last_name%22%2C+%22last_name%22%2C+%22%24name%22%2C+%22name%22%2C+%22%24android_devices%22%2C+%22%24bounce_category%22%2C+%22%24email%22%2C+%22%24ios_devices%22%2C+%22%24marked_spam%22%2C+%22%24phone%22%2C+%22%24unsubscribed%22%2C+%22%24last_seen%22%2C+%22%24predict_grade%22%2C+%22mpx_user_id%22%2C+%22mpx_user_profile_id%22%2C+%22Signed+up+via%22%2C+%22gender%22%2C+%22Account+Status%22%2C+%22autoPlay%22%2C+%22isParentalControls%22%2C+%22parentalControls%22%2C+%22seesoNow%22%2C+%22Paid+Member+Start+Date%22%2C+%22Billing+Status%22%2C+%22Contract+End+Date%22%2C+%22Contract%22%2C+%22%24country_code%22%2C+%22%24timezone%22%5D&behaviors=%5B%7B%22window%22%3A+%2290d%22%2C+%22name%22%3A+%22behavior_116%22%2C+%22event_selectors%22%3A+%5B%7B%22event%22%3A+%22ActivateContract%22%7D%5D%7D%2C+%7B%22window%22%3A+%2230d%22%2C+%22name%22%3A+%22behavior_117%22%2C+%22event_selectors%22%3A+%5B%7B%22event%22%3A+%22Watched+Video%22%7D%5D%7D%5D'
#available endpoint: 2.0/engage(for export people properties)/events(event data)/segmentation/retention(i don't need that shit)

#sending request

def request(api_secret,params,format='json'):
      base_url='https://mixpanel.com/api/2.0/engage?'
      full_url=base_url+unicode_urlencode(params)
      response = requests.get(full_url,auth=(api_secret,'') )
      return response.text

#url_encoding for all the params

def unicode_urlencode(params):
        ''' Convert stuff to json format and correctly handle unicode url parameters'''

        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        result = urllib.parse.urlencode([(k, isinstance(v, str) and v.encode('utf-8') or v) for k, v in params])
        return result



#loop all the page to get all records
def page_results(response, params, global_total):

    fname = "people_export_" + str(int(time.time())) + ".csv"
    has_results = True
    total = 0
    while has_results:
        responser=json.loads(response)['results']
        total+=len(responser)
        has_results=len(responser)== 1000
        df=pd.DataFrame(pd.io.json.json_normalize(responser))

        with open(fname, 'a') as f:
               df.to_csv(f,header=False,index=False)
        print ("%d / %d" % (total, global_total))

        params['page']+=1
        if has_results :
             response=request(api_secret,params)

    print (total==global_total)
    return fname


#to get the session_id and continue request to get full data

def get_results(params):
    response=request(api_secret,params)
    #print (response)
    if json.loads(response)['session_id']:
        print("inital connection established")
        params['session_id'] = json.loads(response)['session_id']
        params['page'] = 0

        global_total = json.loads(response)['total']

        print ("Session id is %s \n" % params['session_id'])
        print ("Here are the # of people %d" % global_total)
    else:
        print(json.loads(response)['error'])

    paged=page_results(response, params, global_total)
    df=pd.read_csv(paged)
    #print(df)
    df.columns=["id","email","timestamp"]
    email_list=df[["email"]]
    return email_list

#%%
####task 1 activate contract email list from 2016.01.01

today = datetime.date.today()
yesterday=today-timedelta(days=1)
start_date = datetime.date(2015,11,1)#today-timedelta(days=7)
diff = yesterday - start_date
length=str(diff.days)

day_range=str(length)+"d"
#%%
selector = '(behaviors["behavior_269"] > 0)'
behaviors =r'[{"window": "'+day_range+'", "name": "behavior_269", "event_selectors": [{"event": "ActivateContract"}]}]'
output_properties='["$email"]'



if not behaviors:
    time_offset = -3
    params = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    params = {'selector': selector, 'behaviors': behaviors,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

df=get_results(params)
df
df.to_csv("Mixpanel-Activate contract -"+start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)


#%%
#####task 2 watched 100 video and rebiil 2+


selector = '(behaviors["behavior_271"] > 2 and behaviors["behavior_272"] > 100)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_271", "event_selectors": [{"event": "BillRecurringPayment", "selector": "(event[\"succeeded\"] == true)"}]}, {"window": "'+day_range+r'", "name": "behavior_272", "event_selectors": [{"event": "Watched Video"}]}]'
output_properties='["$email"]'


if not behaviors:
    time_offset = -3
    watch_parameters = {'selector': selector, 'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    watch_parameters = {'selector': selector, 'behaviors': behaviors, 'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


df3=get_results(watch_parameters)
df3.to_csv("Mixpanel-Watched 100 rebilled 2 email -"+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)
#%%
###taks3 watched video 200+ rebilled 1+
#means (behaviors["behavior_271"] >= 1 and behaviors["behavior_272"] >= 200)
selector = '(behaviors["behavior_271"] >= 1 and behaviors["behavior_272"] >= 200)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_271", "event_selectors": [{"event": "BillRecurringPayment", "selector": "(event[\"succeeded\"] == true)"}]}, {"window": "'+day_range+r'", "name": "behavior_272", "event_selectors": [{"event": "Watched Video"}]}]'
output_properties='["$email"]'

if not behaviors:
    time_offset = -3
    watched_parameters2 = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    watched_parameters2 = {'selector': selector, 'behaviors': behaviors,'output_properties':output_properties, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


df4=get_results(watched_parameters2)
df4.to_csv("Mixpanel-Watched 200 rebilled 1 email -"+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)

#%%
###taks3 watched video 200+ rebilled 3+

selector = '(behaviors["behavior_271"] >= 3 and behaviors["behavior_272"] >= 200)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_271", "event_selectors": [{"event": "BillRecurringPayment", "selector": "(event[\"succeeded\"] == true)"}]}, {"window": "'+day_range+r'", "name": "behavior_272", "event_selectors": [{"event": "Watched Video"}]}]'
output_properties='["$email"]'

if not behaviors:
    time_offset = -3
    watched_parameters2 = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    watched_parameters2 = {'selector': selector, 'behaviors': behaviors,'output_properties':output_properties, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


df4=get_results(watched_parameters2)
df4.to_csv("Mixpanel-Watched 200 rebilled 3 email -"+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)
#%%
#####event 5####
"""
selector = '(behaviors["behavior_271"] >= 3 and behaviors["behavior_322944"] >= 1)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_271", "event_selectors": [{"event": "BillRecurringPayment", "selector": "(event[\"succeeded\"] == true)"}]}, {"window": "'+day_range+r'", "name": "behavior_322944", "event_selectors": [{"event": "Linked Device,Logged In,Sign Up"}]}]'
output_properties='["$email"]'

if not behaviors:
    time_offset = -3
    watched_parameters2 = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    watched_parameters2 = {'selector': selector, 'behaviors': behaviors,'output_properties':output_properties, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


df4=get_results(watched_parameters2)
df4.to_csv("Mixpanel-Watched 200 rebilled 3 linked -"+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)
"""
#%%
#########task 4  for rebill 1+

selector = '(behaviors["behavior_334"] >3)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

output_properties='["$email"]'


if not behaviors:
    time_offset = -3
    rebill_parameters1 = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    rebill_parameters1 = {'selector': selector,'output_properties':output_properties ,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

rebill_df1=get_results(rebill_parameters1)
rebill_df1.to_csv("Mixpanel-Rebill success 3 from "+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)
#%%

############task 5 for rebill 2+
#rebill1 means (behaviors["behavior_334"] > 1)
day_range=str(length)+"d"

selector = '(behaviors["behavior_334"] > 1)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters6 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters6 = {'selector': selector,'output_properties':output_properties, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

#response = request(api_secret,rebill_parameters6)
#response
#print (json.loads(response)["total"])
rebill_df6=get_results(rebill_parameters6)

rebill_df6.to_csv("Mixpanel-Rebill success 1 from "+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)

#%%
day_range=str(length)+"d"

selector = '(behaviors["behavior_334"] > 2)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters6 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters6 = {'selector': selector,'output_properties':output_properties, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


rebill_df6=get_results(rebill_parameters6)
rebill_df6.to_csv("Mixpanel-Rebill success 2 from "+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)
#%%
day_range=str(length)+"d"

selector = '(behaviors["behavior_334"] > 3)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters6 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters6 = {'selector': selector,'output_properties':output_properties, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


rebill_df6=get_results(rebill_parameters6)
rebill_df6.to_csv("Mixpanel-Rebill success 3 from "+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)

#%%
day_range=str(length)+"d"

selector = '(behaviors["behavior_334"] > 6)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "'+day_range+r'", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters6 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters6 = {'selector': selector,'output_properties':output_properties, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


rebill_df6=get_results(rebill_parameters6)
rebill_df6.to_csv("Mixpanel-Rebill success 6 from "+ start_date.strftime("%m.%d.%Y")+" to "+yesterday.strftime("%m.%d.%Y")+".csv",index=False)












#%%
"""
##########################################我是大写的分割线，下面不用query#####################
#########query 2 on people api

selector = '(behaviors["behavior_324"] > 0 and behaviors["behavior_325"] > 5)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "7d", "name": "behavior_324", "event_selectors": [{"event": "ActivateContract"}]}, {"window": "7d", "name": "behavior_325", "event_selectors": [{"event": "Watched Video"}]}]'
output_properties='["$email"]'



if not behaviors:
    time_offset = -3
    parameters = {'selector': selector,'output_properties':output_properties,'as_of_timestamp': int(time.time()) + (time_offset * 3600)}
else:
    time_offset = -3
    parameters = {'selector': selector, 'output_properties':output_properties,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}



df2=get_results(parameters)
df2.to_csv("Mixpanel-Activate contract and watch 5 - "+time.strftime("%m.%d.%Y")+".csv",index=False)




########rebill
selector = '(behaviors["behavior_334"] > 1 and behaviors["behavior_335"] > 0)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "90d", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}, {"window": "90d", "name": "behavior_335", "event_selectors": [{"event": "Linked Devices"}]}]'



if not behaviors:
    time_offset = -3
    rebill_parameters2 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters2 = {'selector': selector, 'output_properties':output_properties ,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

rebill_df2=get_results(rebill_parameters2)
rebill_df2.to_csv("Mixpanel-Rebill success 1 in 90 days and linked devices - "+time.strftime("%m.%d.%Y")+".csv",index=False)

#####rebill

selector = '(behaviors["behavior_334"] > 1 and behaviors["behavior_335"] > 9)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "90d", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}, {"window": "90d", "name": "behavior_335", "event_selectors": [{"event": "Logged In"}]}]'

if not behaviors:
    rebill_parameters3 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters3 = {'selector': selector, 'output_properties':output_properties,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

rebill_df3=get_results(rebill_parameters3)
rebill_df3.to_csv("Mixpanel-Rebill success 1 in 90 days and logged in - "+time.strftime("%m.%d.%Y")+".csv",index=False)

#############rebill
selector = '(behaviors["behavior_334"] > 1 and (properties["campaign"] == "Organic"))'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "90d", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters4 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters4 = {'selector': selector, 'output_properties':output_properties,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

rebill_df4=get_results(rebill_parameters4)
rebill_df4.to_csv("Mixpanel-Rebill success 1 in 90 days and organic - "+time.strftime("%m.%d.%Y")+".csv",index=False)



###############rebill
selector = '(behaviors["behavior_334"] > 1 and behaviors["behavior_335"] > 90)'
    # Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "90d", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}, {"window": "90d", "name": "behavior_335", "event_selectors": [{"event": "Watched Video"}]}]'

if not behaviors:
    rebill_parameters5 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters5 = {'selector': selector, 'output_properties':output_properties,'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}

rebill_df5=get_results(rebill_parameters5)
rebill_df5.to_csv("Mixpanel-Rebill success 1 in 90 days and watched video - "+time.strftime("%m.%d.%Y")+".csv",index=False)

############rebill
selector = '(behaviors["behavior_334"] > 2)'
# Leave 'r' before the behaviors string so that it's interpreted as a string literal to handle escaped quotes
behaviors = r'[{"window": "373d", "name": "behavior_334", "event_selectors": [{"event": "$custom_event:218555", "selector": "(event[\"Active\"] == true)"}]}]'

if not behaviors:
    rebill_parameters6 = {'selector': selector}
else:
    time_offset = -3
    rebill_parameters6 = {'selector': selector,'output_properties':output_properties, 'behaviors': behaviors, 'as_of_timestamp': int(time.time()) + (time_offset * 3600)}


rebill_df6=get_results(rebill_parameters6)
rebill_df6.to_csv("Mixpanel-Rebill success 2 from 01.01.2016 to "+time.strftime("%m.%d.%Y")+".csv",index=False)
"""
