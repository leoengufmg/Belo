import pandas as pd
import pyodbc
import json
from datetime import date
from datetime import datetime
import time
from LoadConfigTool import LoadConfigTool
import requests
from requests.auth import HTTPBasicAuth
import threading

ConfigApiUrl=""
ConfigApi=""
ConfiDbReport=""
ConfigDbUs=""
########
conndb=None
connreport=None

 
def LoadConfigLocal(env):

    global ConfigApiUrl
    global ConfigApi
    global ConfiDbReport
    global ConfigDbUs
    global conndb
    global connreport 


    #################
    ConfigApiUrl,ConfigApi,ConfiDbReport,ConfigDbUs,conndb, connreport = LoadConfigTool(env)
          

def processAll(amount,concurrent):
    result = 1

    while(result>0):
        result = AddContractAll(amount,concurrent)

def AddContractAll(amount, concurrent):
    global connreport 

    query='SELECT top {} IdContract,DataContractApi,IdStateContractApi,TypeContractApi,ProcessedStatusContractApi,IdContractApi FROM dbo.ContractApi WHERE ProcessedStatusContractApi=0'.format(amount)
    cursor = connreport.cursor()
    result = cursor.execute(query)
    records = cursor.fetchall()
    insertObject = []
    ThreadArray = []
    ##################
    #columnNames = [column[0] for column in cursor.description]
    if(concurrent==0):
        for record in records:
            IdContract = record[0]
            DataContractApi = record[1]
            IdStateContractApi = record[2]
            TypeContractApi = record[3]
            ProcessedStatusContractApi = record[4]
            IdContractApi = record[5]

            if(TypeContractApi=='add'):
                AddContract(DataContractApi,IdContract,ProcessedStatusContractApi,IdStateContractApi,IdContractApi)
                



    if(concurrent==1):
        for record in records:
            IdContract = record[0]
            DataContractApi = record[1]
            IdStateContractApi = record[2]
            TypeContractApi = record[3]
            ProcessedStatusContractApi = record[4]
            IdContractApi = record[5]


            if(TypeContractApi=='add'):
                t =  threading.Thread(target=AddContract, args=(DataContractApi,IdContract,ProcessedStatusContractApi,IdStateContractApi,IdContractApi))
                ThreadArray.append(t)

        
        for Thread in ThreadArray:
            Thread.start()
            time.sleep(1/10)

        for Thread in ThreadArray:
            Thread.join()
    
    print(len(records))
    return len(records)
    print('_______________________________FINISH RUN_________________________________________')



            #AddContract(DataContractApi,IdContract,ProcessedStatusContractApi,IdStateContractApi,IdContractApi)

        #insertObject.append( dict( zip( columnNames , record )))
    ###################

   

def AddContract(DataContractApi,IdContract,ProcessedStatusContractApi,IdStateContractApi,IdContractApi):
    global ConfigApi
    global connreport
    global ConfigApiUrl
    #####################################
    SendTimestamp = str(time.time())
    datajson=json.loads(DataContractApi)
    #####################################
    datajson = json.dumps(datajson)
    callApi("AddContract", datajson,IdContractApi,IdContract)



def callApi(action,payload,IdContractApi,IdContract):
    global ConfigApi
    global ConfigApiUrl
    global connreport 

    text =''
    status_code=0
    msg = ''
    codeMsg = 0
    #########################
    datetimeInitial=""
    datetimeFinal=""
    url = ConfigApi['url']
    user = ConfigApi['user']
    password = ConfigApi['password']
    Authorization = ConfigApi['Authorization']
    endpoint=""
    #########################
    for row in ConfigApiUrl:
        if(row['action']==action):
            endpoint = row['endpoint']
    
    endpoint = url + endpoint 
    ########################

    ########################################################################################################################


    payloadJson= json.loads(payload)
    
    #if(payloadJson['OptionInfo'] != None):
    OptionInfo= payloadJson['OptionInfo'][0]

    ContractBillToCustomersInfo=[]
    ContractInChargeCustomersInfo=[]
        
    ContractBillToCustomersInfo = payloadJson['ContractBillToCustomersInfo']
    ContractInChargeCustomersInfo = payloadJson['ContractInChargeCustomersInfo']

    #ContractInChargeCustomersInfo.append( OptionInfo['ContractInChargeCustomersInfo'] )

        
        #payloadJson['OptionInfo']={}
        
        #UpdateContractTableInChargeCustomersInfo=[]
            #UpdateContractTableBillToCustomersInfo=OptionInfo['UpdateContractTableBillToCustomersInfo']
            #UpdateContractTableBillToCustomersInfo=[]


    del payloadJson["ContractBillToCustomersInfo"]
    del payloadJson["ContractInChargeCustomersInfo"]
    #del OptionInfo["ContractInChargeCustomersInfo"]

    OptionInfo['ContractBillToCustomersInfo']=ContractBillToCustomersInfo
    OptionInfo['ContractInChargeCustomersInfo']=ContractInChargeCustomersInfo

    payloadJson['OptionInfo'] = OptionInfo

    payload=json.dumps(payloadJson)
    print(payload)

        #payload=json.dumps(payloadJson)


    #######################################################################################################################

    try:
        cursor = connreport.cursor()
        payload = payload.replace("'", "''")
        #print("IdContract: ",IdContract)
        #print(payload)
        datetimeInitial = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
        myobj = {'Data': payload}
        #print(myobj)
        files=[]
        headers = {'Authorization': Authorization }

        response = requests.request("POST", url=endpoint, headers=headers, data=myobj, files=files)
        #print(response.text)

            # response = requests.post(
            # endpoint,
            # auth=HTTPBasicAuth(user,password ),data=myobj,headers=headers)
        datetimeFinal = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        status_code = response.status_code 
        text = response.text 




        try:
            #text = re.sub(re.compile('<.*?>'), '', text)
            text = text.replace("'", "")
            codeMsg = json.loads(text)['code']
            msg = json.loads(text)['retMsg']
            msg=msg.replace("'", "")
            print(msg)
        
        except Exception as e:
            msg = text[-30:]
            msg=msg.replace("'", "")
            msg=msg.replace('"', '')
           



            #####################################################

        query='''
                INSERT INTO dbo.ContractApiLog
                (
                    IdContractApi,
                    DateCallContractApiLog,
                    DateAnswerContractApiLog,
                    StatusCodeContractApiLog,
                    StatusCodeApiContractApiLog,
                    PayloadContractApiLog,
                    BodyResultContractApiLog,
                    ResultMessageContractApiLog
                )
                VALUES
                (  {},'{}','{}','{}','{}','{}','{}','{}')

            '''.format(IdContractApi,datetimeInitial,datetimeFinal,status_code,codeMsg,str(payload),text,msg)
        
        #print(query)
        cursor.execute(query)
            ##############################
        queryUpdate ='''
            UPDATE dbo.ContractApi SET ProcessedStatusContractApi=1 WHERE IdContractApi={}
            '''.format(IdContractApi)
        cursor.execute(queryUpdate)

            ##############################
        queryUpdate ='''
            UPDATE dbo.Contract SET ReportSentToSource=0 WHERE IdContract={}
            '''.format(IdContract)
        cursor.execute(queryUpdate)

            ##############################
        # queryUpdate ='''
        #     EXEC [dbo].[ContractDistributeResult] {}
        #     '''.format(IdContract)
        # cursor.execute(queryUpdate)
            
            ##############################
        if(codeMsg=='500'):
            queryUpdate ='''
                UPDATE dbo.Contract SET IdStateDomain=2 WHERE IdContract={}
                '''.format(IdContract)
            cursor.execute(queryUpdate)


        #####################################################

    except Exception as e:
        print('Error to call ',  str(e))
        error = str(e).replace("'", "").replace('\n', ' ').replace('\r', '')
        queryUpdate ='''
            INSERT INTO dbo.LogProcess
                (
                    ProcessLogProcess,
                    MessageLogProcess,
                    KeyRecord
                )
                VALUES
                ('{}','{}',{} )
            '''.format('callApi AddContract',error,IdContract)
        cursor.execute(queryUpdate)



LoadConfigLocal('dev')
#AddContractAll(5000)
processAll(100,1)