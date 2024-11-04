# encoding:utf-8
import requests 

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=UCibaZ4yxoZu64bEUvCNYv7p&client_secret=35gBtom8XTjoiIOSIh6G41eHoIxeVITd'
response = requests.get(host)
if response:
    print(response.json())