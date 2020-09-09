import requests
import json
from sys import argv, exit
import time
from datetime import date, timedelta
##Change the login url for test
def authorise(client_id, client_secret, username, password):
    #api_headers = {'Content-type': 'application/json'}
    body={"grant_type":"password","client_id":client_id,"client_secret":client_secret,"username":username,"password":password}
    try:
        login_url="https://test.salesforce.com/services/oauth2/token"
        post_response = requests.post(url = login_url,params=body)#data=json.dumps(body), headers = api_headers)
        json_data = json.loads(post_response.text)
        print(json_data)
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response.status_code != 200:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("Access Token Successfully received")
    return json_data['access_token'] 

def get_project_id(auth_token, project_name):
    api_headers = {'Content-type': 'application/json', 'Authorization': 'OAuth '+auth_token}
    try:
        query_url="https://bpcommunity--gptdev.my.salesforce.com/services/data/v46.0/query/?q=SELECT+id+from+C4E_Project__c+"+"WHERE+Name+LIKE+'" + project_name.replace(' ','+')+"'"
        get_response = requests.get(url = query_url, headers = api_headers)
        json_data = json.loads(get_response.text)
    except Exception as e:
        print("error: ",e)
        exit(1)
    if get_response.status_code != 200:
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)
    elif json_data['totalSize'] != 1:
        print('Error! Message: Either no record was returned or more than one matching record is found')
        exit(1)
    print("Matching Project Id retrieved")
    return [json_data['records']['Id'],json_data['records']['C4E_Namespace__c']] ##Confirm that this accesss works


def create_release(auth_token, proj_id, proj_namespace, release_rectyp, requested_date):
    api_headers = {'Content-type': 'application/json', 'Authorization': 'OAuth '+auth_token}
    body={"RecordTypeId":release_rectyp,"C4E_Release_Name__c":proj_namespace+ " - Standard Release - " + requested_date.remove("-"),"Project__c":proj_id,"C4E_Stage__c":"Prod"}
    try:
        post_url="https://bpcommunity.my.salesforce.com.my.salesforce.com/services/data/v46.0/sobjects/C4E_Release__c"   
        post_response = requests.post(url = post_url,data=json.dumps(body), headers = api_headers)
        json_data = json.loads(post_response.text)
        
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response.status_code != 200:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("Release successful created")
    return json_data['id']

def create_mock_record(auth_token):
    api_headers = {'Content-type': 'application/json', 'Authorization': 'OAuth '+auth_token}
    body_mr={"BPG_Text1__c":"Text Test 1","BPG_Text2__c":"Text Test 2","BPG_Text3__c":"Text Test 3"}
    try:
        post_url_prod="https://bpcommunity--gptdev.my.salesforce.com/services/data/v46.0/sobjects/BPG_Mock_Object__c"   
        post_response_prod = requests.post(url = post_url_prod,data=json.dumps(body_mr), headers = api_headers)
        json_data = json.loads(post_response_prod.text)
        print(json_data)
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response_prod.status_code != 200:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("Mock record successfully created")

def create_deployments(auth_token,release_id,requested_date):
    api_headers = {'Content-type': 'application/json', 'Authorization': 'OAuth '+auth_token}
    [dd, mm, yy] = requested_date.split("-")
    preprod=date.today()
    sit=date.today()
    prod = date(2000+int(yy), int(mm), int(dd))  ## Check format of date, remove 2000+ if yyyy
    if prod.weekday() == 0:
        preprod = prod - timedelta(days=3)
        sit = prod - timedelta(days=4)
    elif prod.weekday() == 3:
        preprod = prod - timedelta(days=1)
        sit = prod - timedelta(days=2)
    else:
        print('Error! Message: Dates do not match reference')
        exit(1)
    body_prod={"RecordTypeId":"0124J000000Ym6JQAS","C4E_Release__c":release_id,"C4E_Status__c":"Dates Agreed","C4E_Date__c":str(prod)}
    body_preprod={"RecordTypeId":"0124J000000Ym6EQAS","C4E_Release__c":release_id,"C4E_Status__c":"Dates Agreed","C4E_Date__c":str(preprod)}
    body_sit={"RecordTypeId":"0124J000000Ym6OQAS","C4E_Release__c":release_id,"C4E_Status__c":"Dates Agreed","C4E_Date__c":str(sit)}
    
    ################PROD
    try:
        post_url_prod="https://bpcommunity.my.salesforce.com.my.salesforce.com/services/data/v46.0/sobjects/C4E_Deployment__c"   
        post_response_prod = requests.post(url = post_url_prod,data=json.dumps(body_prod), headers = api_headers)
        json_data = json.loads(post_response_prod.text)
        
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response_prod.status_code != 201:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("Prod Deployment record successfully created")

    #################PREPRDOD
    try:
        post_url_preprod="https://bpcommunity.my.salesforce.com.my.salesforce.com/services/data/v46.0/sobjects/C4E_Deployment__c"   
        post_response_preprod = requests.post(url = post_url_preprod,data=json.dumps(body_preprod), headers = api_headers)
        json_data = json.loads(post_response_preprod.text)
        
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response_preprod.status_code != 200:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("PreProd Deployment record successfully created")

    ########SIT
    try:
        post_url_sit="https://bpcommunity.my.salesforce.com.my.salesforce.com/services/data/v46.0/sobjects/C4E_Deployment__c"   
        post_response_sit = requests.post(url = post_url_sit,data=json.dumps(body_sit), headers = api_headers)
        json_data = json.loads(post_response_sit.text)
        
    except Exception as e:
        print("error: ",e)
        exit(1)
    if post_response_sit.status_code != 200:                                                    
        if 'message' in json_data:
            print('Error! Message: ', json_data['message'])
        exit(1)                       
    print("SIT Deployment record successfully created")    
