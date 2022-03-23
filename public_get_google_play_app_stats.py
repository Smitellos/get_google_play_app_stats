import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
import dateutil.relativedelta
import json
import os
from io import StringIO
#Install python lib for oauth2client: https://developers.google.com/api-client-library/python/
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build


#Google api fucntion
def download_report():
    private_key = json.loads(open(json_file).read())['private_key']
    credentials = SignedJwtAssertionCredentials(client_email, private_key,
    'https://www.googleapis.com/auth/devstorage.read_only')
    storage = build('storage', 'v1', http=credentials.authorize(Http()))
    bytes_data = storage.objects().get_media(bucket=developer_bucket_id,object=report_to_download).execute()
    s = str(bytes_data,'utf-16')
    data = StringIO(s)


#Variables for application
package_name = "your.package.name"
#Change package name appropriately to your google console

#Manual https://support.google.com/googleplay/android-developer/answer/6135870

#Static variables
#Can change accordingly to your cloud storage https://console.cloud.google.com/storage/browser/pubsite_prod_rev_.../

#Developer bucket id with data
developer_bucket_id = "pubsite_prod_rev_..."
#Service account email
#Need at least role=readonly in top level for all applications in play.google.com
client_email = 'example@yourprojectname.iam.gserviceaccount.com'
#Json file
json_file = '/opt/scripts/yourprojectname-code.json'
#Dimension for download
dimension = "overview"
#Location in google.cloud
cloud_location = "stats/installs/installs"


#Get dates for download links and names
current_month = int(f"{datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1):%Y%m}")
previous_month = int(f"{datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-2):%Y%m}")
scatter_name_current_month='Active users per '+str(current_month)+''
scatter_name_previous_month='Active users per '+str(previous_month)+''

#Download current period
report_to_download = ''+(cloud_location)+'_'+(package_name)+'_'+str(current_month)+'_'+(dimension)+'.csv'
current_df = pd.read_csv(download_report())

#Download previous period
report_to_download = ''+(cloud_location)+'_'+(package_name)+'_'+str(previous_month)+'_'+(dimension)+'.csv'
previous_df = pd.read_csv(download_report())


fig = go.Figure()

#Create plots from pandas data
fig.add_trace(
    go.Scatter(x=current_df['Date'], y=current_df['Active Device Installs'], name=scatter_name_current_month))

fig.add_trace(
    go.Scatter(x = previous_df['Date'], y = previous_df['Active Device Installs'], name=scatter_name_previous_month,xaxis="x2",mode='lines',
    line=dict(color="#BBE4FA")))

#Set dimensions for x overlaying and display parameters
fig.update_layout(
    yaxis=dict(
        gridcolor='rgb(230,230,230)'
    ),
    xaxis=dict(
        titlefont=dict(
            color="#1f77b4"
        ),
        tickfont=dict(
            color="#1f77b4"
        ),
        
    ),
    xaxis2=dict(
        titlefont=dict(
            color="#ffffff"
        ),
        tickfont=dict(
            color="#ffffff"
        ),
        overlaying="x",
        side="top"
    )
)

#Update layout
fig.update_layout(title='Active users APPNAME',
                   plot_bgcolor='rgb(255,255,255)',
                   width=1400,
                   height=700,
                   showlegend=True)
#Print graph
#fig.show()
cwd = os.getcwd()
writedir=''+(cwd)+''+(package_name)+'.png'
fig.write_image(writedir)