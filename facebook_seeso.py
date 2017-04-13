# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:24:35 2017

@author: Jeremy

This script is for Facebook api.
    export the report for some specific date
"""

#please install facebookads.api before using
from __future__ import print_function
import os
#os.chdir(r"C:\ProgramData\Anaconda3\Lib\site-packages\facebookads")
from facebookads.api import FacebookAdsApi
#from facebookads.adobjects.ad import Ad
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.adobjects.adreportrun import AdReportRun
from facebookads.objects import AdAccount
import datetime
import time
import pandas as pd

import sys
path = r"C:\Users\jeremy\Desktop\Seeso\daily Facebook"
os.chdir(path)

subdirectory =(datetime.datetime.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')

try:
    os.mkdir(path + '\\raw_data\\'+subdirectory)
except Exception:
    pass

def export_report_facebook(config): 
    #pull report thru facebook api  
    # Get insights stats for this account id
    account_id=config[0]
    param=config[1]
    count=config[-1]
    account = AdAccount(account_id)
    async_job = account.get_insights(params=param, async=True)    
    async_job.remote_read()    
    while async_job[AdReportRun.Field.async_percent_completion] < 100: 
        time.sleep(20)
        print(AdReportRun.Field.async_percent_completion)
        async_job.remote_read()
        #print(async_job)
    #read file in bulk
    #pd.read_csv("""https://www.facebook.com/ads/ads_insights/export_report/?report_run_id=%s"""%async_job['report_run_id']+"&name=myreport&format=csv&access_token=" + my_access_token,chunksize=10**5)
    download_address="""https://www.facebook.com/ads/ads_insights/export_report/?report_run_id=%s"""%async_job['report_run_id']+"&format=csv&access_token=" + my_access_token
    chunksize=10**5
    downloadpath= path + "\\raw_data\\"+subdirectory
    for chunk in pd.read_csv(download_address,chunksize=chunksize):
        chunk.ix[chunk["Placement"] == 'Instagram Feed on Mobile Devices',"Placement"] ='Instagram'
        chunk.ix[chunk["Placement"] != 'Instagram',"Placement"] ='Facebook'
        chunk=chunk[['Reporting Starts', 'Reporting Ends', "Placement", 'Campaign Name',
       'Ad Name', 'Ad Set Name','Clicks (All)', 'Impressions', 'Amount Spent (USD)',"Website Purchases"]]
        chunk.to_csv(downloadpath+"\\facebook_%s.csv"%(count),index=False)

#%%
# To initialize, pass the following values
# 1) Pass api key values to make api calls
def generate_params(start,end,interval,account_id):
    
    start_date =datetime.datetime.strptime(start,"%Y-%m-%d")
    end_date = datetime.datetime.strptime(end,"%Y-%m-%d")
    # 2) Specify the fields we need from the DailyReport
    myfields = [AdsInsights.Field.clicks, AdsInsights.Field.impressions, AdsInsights.Field.spend, 
                AdsInsights.Field.date_start, AdsInsights.Field.date_stop,
                AdsInsights.Field.campaign_name, AdsInsights.Field.ad_name, AdsInsights.Field.adset_name, AdsInsights.Field.actions]
                # AdsInsights.Field.actions    
    # 3) Specify the parameters we need in the URL   
                          #'date_preset': AdsInsights.DatePreset.yesterday
    def param_time_interval(myfields,start_date,end_date):
        params = {'level': 'ad',
                  'fields': myfields,
                  'time_range': {'since': start_date,'until':end_date},
                  'time_increment': 1,
                  'breakdowns': ['placement']
                  }
        return params   
    timeline = []
    count=0
    if interval == None:
        start_date=start_date.strftime('%Y-%m-%d')
        end_date=end_date.strftime('%Y-%m-%d')
        pa=param_time_interval(myfields,start_date,end_date)
        timeline.append([account_id,pa,str(count)])
    else:
        end = start_date + datetime.timedelta(days=interval)
        if end > end_date:
            start_date1=start_date.strftime('%Y-%m-%d')
            end_date1=end_date.strftime('%Y-%m-%d')
            pa=param_time_interval(myfields,start_date1,end_date1)
            timeline.append([account_id,pa,str(count)])
        else:
            start = start_date
            while end < end_date:
                start1=start.strftime('%Y-%m-%d')
                end1=end.strftime('%Y-%m-%d')
                pa=param_time_interval(myfields,start1,end1)
                timeline.append([account_id,pa,str(count)])
                start = end + datetime.timedelta(days=1)
                end = start + datetime.timedelta(days=interval)
                count+=1
            start1=start.strftime("%Y-%m-%d")
            end_date1=end_date.strftime("%Y-%m-%d")
            pa=param_time_interval(myfields,start1,end_date1)
            timeline.append([account_id,pa,str(count)])
    return timeline              

# 4) Pass the account id 
my_app_id = 'Your APP ID'
my_app_secret = 'Your APP secret'
my_access_token = 'Your Access Token'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
account_id='account_id'
##run the file
Month_ago = datetime.datetime.today()-datetime.timedelta(days=31)
since = (Month_ago).strftime("%Y-%m-%d")
until = (datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
interval=1
timeline=generate_params(since,until,interval,account_id)
start = time.time()
for i in timeline:
    export_report_facebook(i)
    time.sleep(90)
print('Test:', time.time() - start)

#combine the file and save it
downloadpath = path + "\\raw_data\\"+subdirectory
chunksize=10**5
list_csv=[file for file in os.listdir(downloadpath) if ".csv" in file]         
if not os.path.isfile(path + "\\raw_data"+'\\Facebook_%s-%s.csv'%(since,until)) :
    for i in range(len(list_csv)):
        for chunk in pd.read_csv(downloadpath+"\\"+list_csv[i], chunksize=chunksize,encoding="ISO8859-1",dtype=str):
        #for chunk in pd.read_csv(downloadpath+'\\facebook_'+str(i)+".csv", chunksize=chunksize,encoding="ISO8859-1",dtype=str):
            chunk.to_csv(path + "\\raw_data"+'\\Facebook_%s_%s.csv'%(since,until),mode='a',index=False)
    else:
        print("Take care. File exists.")
        sys.exit()
         
file = pd.read_csv(path + "\\raw_data\\Facebook_final.csv")
file1 = pd.read_csv(path + "\\raw_data"+'\\Facebook_%s_%s.csv'%(since,until))
file = file[pd.to_datetime(file['Reporting Starts']) < Month_ago]
file = pd.concat([file,file1])
file.to_csv(path+"\\raw_data\\Facebook_final.csv")