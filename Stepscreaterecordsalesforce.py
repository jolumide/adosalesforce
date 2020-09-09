import requests
import json
import time
from sys import argv, exit
from actions import *
from datetime import datetime

#Arguments

username='olumide.akinwande@bp.com.community.gptdev'
password='0lum1dE£4%2014'
client_id="3MVG95AcBeaB55lVC4ph4E3buPW7Texcr7qDeNnXA47bwtTa3W0hIKb5dZf9CCnnZuvkmjQKbOYBzExCAre0N"
client_secret="E0D79A342987B8F876EB8E7BE3A889AC49726C006E09646BF031D1DA00C5666D"
#project_name=argv[5]
#requested_date=argv[6] #format dd-mm-yy
#release_rectyp=arg[7]


#Get Auth token

auth_token = authorise(client_id, client_secret, username, password)

#Create Mock records

create_mock_record(auth_token)
