#!/usr/bin/env python36
import requests, json, logging
from datetime import datetime, timedelta
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
from sys import exit

NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
FIFTEEN_MINUTES_AGO = datetime.now() - timedelta(minutes=15)
FIFTEEN_MINUTES_AGO = FIFTEEN_MINUTES_AGO.strftime('%Y-%m-%d %H:%M:%S')

GRAYLOG_SERVER = "graylog.you.com"
GRAYLOG_PORT = 11589
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.addHandler(GelfUdpHandler(host=GRAYLOG_SERVER, port=GRAYLOG_PORT))

"""
Get API_KEY from https://lastpass.com/company/#!/settings/enterprise-api
"""
API_KEY = ""
API_URL = "https://lastpass.com/enterpriseapi.php"

REQUEST = {}
# Get cid from https://lastpass.com/company/#!/settings/enterprise-api
REQUEST['cid'] = ''
REQUEST['provhash'] = API_KEY
REQUEST['cmd'] = "reporting"
REQUEST['data'] = {}
REQUEST['data']['from'] = NOW
REQUEST['data']['to'] = FIFTEEN_MINUTES_AGO


r = requests.post(API_URL, data=json.dumps(REQUEST))
r_json = json.loads(r.text)
r_status = r_json['status']
if r_status == 'OK':
    logging.info("Successfully authenticated against API")
else:
    logging.error("Failed to download activity: {}").format(str(r_json['errors']))

if r_json['data'] == []:
    logging.info("No data to download")
    exit(0)
try:

    COUNTER = 1
    # API only returns 10000 events
    for i in range(10000):  
        try:
            EVENT_ID = "Event%i" %(COUNTER)
            USERNAME = r_json['data'][EVENT_ID]['Username']
            ACTION = r_json['data'][EVENT_ID]['Action']
            IPADDR = r_json['data'][EVENT_ID]['IP_Address']
            DATA = r_json['data'][EVENT_ID]['Data']

            if ACTION == "Master Password Reuse":
                logging.critical("Detected Master Password Reuse for {}".format(USERNAME))
            else:
                logging.info("{} from {} || {} on {} ".format(str(USERNAME), str(IPADDR), str(ACTION), str(DATA)))
            COUNTER += 1
        except Exception as err:
            logging.error(str(err))

except Exception as err:
    logging.error(str(err))
