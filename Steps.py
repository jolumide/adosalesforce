import requests
import json
import time
from sys import argv, exit
from actions import *
from datetime import datetime

#Arguments

username=argv[1]
password=argv[2]
client_id=argv[3]
client_secret=argv[4]
project_name=argv[5]
requested_date=argv[6] #format dd-mm-yy
release_rectyp=arg[7]


#Get Auth token

auth_token = authorise(client_id, client_secret, username, password)

#Get Project ID

[proj_id, proj_namespace] =get_project_id(auth_token, project_name)

#Create Release record

release_id= create_release(auth_token, proj_id, proj_namespace, release_rectyp, requested_date)

#Create Deployment records

create_deployments(auth_token,release_id,requested_date)
