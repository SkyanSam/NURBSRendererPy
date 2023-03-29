from __future__ import print_function
import platform,socket,re,uuid,json,psutil,logging
from numba import cuda
import cpuinfo
import os.path
import httplib2
import os
import string
from apiclient import discovery
from google.oauth2 import service_account
from raytracetype import *

def getComputerSpecifications() -> str:
    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        architecture = platform.machine()
        ram = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        gpu = cuda.get_current_device()
        cpu = cpuinfo.get_cpu_info()["brand_raw"]
        return f"{system} {release} v{version} {architecture} {ram} {cpu} {gpu}"
    except Exception as e:
        logging.exception(e)

def getMemory(): # ram i think in MiB
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

#def printGpuAttributes():
    #device = cuda.get_current_device()
    #attribs= [name.replace("CU_DEVICE_ATTRIBUTE_", "") for name in dir(enums) if name.startswith("CU_DEVICE_ATTRIBUTE_")]
    #for attr in attribs:
        #print(attr, '=', getattr(device, attr))

# https://denisluiz.medium.com/python-with-google-sheets-service-account-step-by-step-8f74c26ed28e
def get_sheets_api_service():
    scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
    secret_file = os.path.join(os.getcwd(), 'client_secret.json')
    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
    #service = discovery.build('sheets', 'v4', credentials=credentials)
    try:
        service = discovery.build('sheets', 'v4', credentials=credentials)
        return service
    except:
        DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = discovery.build('sheets', 'v4', credentials=credentials, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        return service

def getFirstEmptyRowByColumnArray():
    values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='A:A').execute()["values"]
    return len(values) + 1

def update_sheets(values, range_name=""):
    if (range_name == ""):
        firstRow = getFirstEmptyRowByColumnArray()
        lastRow =  firstRow + len(values) - 1
        firstCol = "A"
        lastCol = string.ascii_uppercase[len(values[0]) - 1]
        range_name = f'Sheet1!{firstCol}{firstRow}:{lastCol}{lastRow}'
        print(range_name)
    data = {
        'values' : values 
    }
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()


def get_avg(arr):
    sum = 0
    for x in arr:
        sum += x
    sum /= len(arr)
    return sum

def send_sample():
    pc_specs = getComputerSpecifications()
    ctrl_avg_dt = get_avg(ctrl_dt_measures)
    ctrl_avg_ra = get_avg(ctrl_render_accuracy_measures)
    nurbs_avg_dt = get_avg(nurbs_dt_measures)
    nurbs_avg_ra = nurbs_render_accuracy_measures[0]#get_avg(nurbs_render_accuracy_measures)
    ctrl_avg_mem = get_avg(ctrl_memory_measures) # in MiB
    nurbs_avg_mem = get_avg(nurbs_memory_measures)
    id = 1
    update_sheets([[id, pc_specs, ctrl_avg_dt, ctrl_avg_ra, ctrl_avg_mem, nurbs_avg_dt, nurbs_avg_ra, nurbs_avg_mem]])

def append_dt(dt):
    match raytraceType:
        case RaytraceType.Control:
            ctrl_dt_measures.append(dt)
        case RaytraceType.NURBS:
            nurbs_dt_measures.append(dt)

def append_render_accuracy(acc):
    match raytraceType:
        case RaytraceType.Control:
            ctrl_render_accuracy_measures.append(acc)
        case RaytraceType.NURBS:
            nurbs_render_accuracy_measures.append(acc)

def append_memory():
    mem = getMemory()
    match raytraceType:
        case RaytraceType.Control:
            ctrl_memory_measures.append(mem)
        case RaytraceType.NURBS:
            nurbs_memory_measures.append(mem)

def setGlobals():
    global spreadsheet_id
    global ctrl_dt_measures
    global nurbs_dt_measures
    global ctrl_memory_measures
    global nurbs_memory_measures
    global ctrl_render_accuracy_measures
    global nurbs_render_accuracy_measures
    global service
    spreadsheet_id = '1dWaji-rcC7qRwYbv3mmyrtJqJ7cCMDM3enGj7G9wYeo'
    ctrl_dt_measures = [0.5,0.4]
    nurbs_dt_measures = []
    ctrl_memory_measures = [0.5,0.4]
    nurbs_memory_measures = []
    ctrl_render_accuracy_measures = [1,2]
    nurbs_render_accuracy_measures = [1,2]
    service = get_sheets_api_service()