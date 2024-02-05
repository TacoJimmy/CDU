#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time 
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import logging
import datetime
import json
import schedule 

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

def GatMB_TCP(ip,id):
    try:
        master = modbus_tcp.TcpMaster(host=ip)
        master.set_timeout(5.0)
        CDU_Data = master.execute(id, cst.READ_HOLDING_REGISTERS, 0, 10)
        
        return CDU_Data
    except:
        logger.error('error')


def TimeFormat():
    date_now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    DateTime = date_now.strftime('%Y/%m/%d %H:%M:%S')
    
    return DateTime

def Savejson(CDU_Data):
    with open("output.json", "w") as f:
        json.dump(CDU_Data, f, indent = 4)

def Job():
    TimeInfo = TimeFormat()
    DataInfo = GatMB_TCP("127.0.0.1",1)
    CDUInfo = {
            "time": TimeInfo,
            "data": DataInfo
        }
    Savejson(CDUInfo)

schedule.every(10).seconds.do(Job)  

if __name__ == '__main__':
    
    while True:  
        schedule.run_pending()  
        time.sleep(1)  
    


