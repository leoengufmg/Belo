import pandas as pd
import pyodbc
import json
from datetime import date
from datetime import datetime
import time
import os


def LoadConfigTool(env):

    cwd = os.getcwd()
    print(cwd)

    #############################################################################
    if(env=='dev2'):
        with open(cwd+'\\'+'US\Connections\dev2\ApiUrls.json') as server_file:
            ConfigApiUrl = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev2\ConfigApi.json') as server_file:
            ConfigApi = json.load(server_file)
        
        with open(cwd+'\\'+'US\Connections\dev2\ConfigDatabaseReport.json') as server_file:
            ConfiDbReport = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev2\ConfigDatabaseUS.json') as server_file:
            ConfigDbUs = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev2\ConfigDatabaseView.json') as server_file:
            ConfigDbView = json.load(server_file)

    #############################################################################
    if(env=='dev'):
        with open(cwd+'\\'+'US\Connections\dev\ApiUrls.json') as server_file:
            ConfigApiUrl = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev\ConfigApi.json') as server_file:
            ConfigApi = json.load(server_file)
        
        with open(cwd+'\\'+'US\Connections\dev\ConfigDatabaseReport.json') as server_file:
            ConfiDbReport = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev\ConfigDatabaseUS.json') as server_file:
            ConfigDbUs = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\dev\ConfigDatabaseView.json') as server_file:
            ConfigDbView = json.load(server_file)


    #############################################################################
    if(env=='test'):
        with open(cwd+'\\'+'US\Connections\\test\ApiUrls.json') as server_file:
            ConfigApiUrl = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\\test\ConfigApi.json') as server_file:
            ConfigApi = json.load(server_file)
        
        with open(cwd+'\\'+'US\Connections\\test\ConfigDatabaseReport.json') as server_file:
            ConfiDbReport = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\\test\ConfigDatabaseUS.json') as server_file:
            ConfigDbUs = json.load(server_file)

        with open(cwd+'\\'+'US\Connections\\test\ConfigDatabaseView.json') as server_file:
            ConfigDbView = json.load(server_file)


    ################################################################################  

    conndb = pyodbc.connect('DRIVER='+ConfigDbUs['driver']+
                      ';Server='+ConfigDbUs['server']+
                      ';PORT=1433;DATABASE='+ConfigDbUs['database']+
                      ';UID='+ConfigDbUs['user']+
                      ';PWD='+ConfigDbUs['password'] )
                      #';Authentication='+ConfigDbUs['Authentication']) 

    conndb.autocommit = True
    #######

    connreport = pyodbc.connect('DRIVER='+ConfiDbReport['driver']+
                      ';Server='+ConfiDbReport['server']+
                      ';PORT=1433;DATABASE='+ConfiDbReport['database']+
                      ';UID='+ConfiDbReport['user']+
                      ';PWD='+ConfiDbReport['password']+';MARS_Connection=yes')
                      #';Authentication='+ConfiDbReport['Authentication']+';MARS_Connection=yes')
    
    connreport.autocommit = True
    #######

    return ConfigApiUrl,ConfigApi,ConfiDbReport,ConfigDbUs,conndb, connreport

#pyLoadConfigTool('dev')