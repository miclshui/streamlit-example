import requests
import json
#import re

url = "https://eth-script-indexer-eca25c4cf43b.herokuapp.com/api/ethscriptions/owned_by/"
max_retries = 10
expected_keys = {"p", "op", "tick", "id", "amt"}
result="符合条件的 id：\n"
rcount=0
minta="646174613a2c7b2270223a226572632d3230222c226f70223a226d696e74222c227469636b223a2265746873222c226964223a22"
mintb="222c22616d74223a2231303030227d"
def checkAddress(address):
  for _ in range(max_retries):
    try:
      response = requests.get(url + address)
      if response.status_code == 200:
         return response
      else:
        print("接收到的响应状态码不是200。正在重试...")
    except requests.exceptions.RequestException as e:
      print(f"发送请求时遇到错误: {e}。正在重试...")
  print(f"在 {max_retries} 次尝试后，未能获得成功响应。")
  return False


def checkResponse(response):
  response_data = response.json()
  valid_ids = []  # 创建一个新的列表来存储所有符合条件的id
  for i in response_data:
    if 'eths' in str(i) :
      content_uri = i.get('content_uri', '')
      str2=content_uri.encode('utf-8').hex()
      if content_uri.startswith('data:,'):
         if ' ' not in str(content_uri):
          try:
            json_data = json.loads(content_uri[6:])
            if isinstance(json_data, dict):
              id_value = json_data.get('id', '')
              tick_value = json_data.get('tick', '')
              p = json_data.get('p', '')
              op = json_data.get('op', '')
              amt = json_data.get('amt', '')
              # 检查 JSON 数据的键的集合是否等于期望的键的集合
            
            if set(json_data.keys()) == expected_keys and \
                    minta + str(json_data["id"]).encode('utf-8').hex() + mintb==str2 and \
                    not str(json_data["id"]).startswith("0") and \
                    1 <= int(id_value) <= 21000 and \
                    tick_value == 'eths' and p == 'erc-20' and op == 'mint' and amt == '1000':
              
              valid_ids.append(int(id_value))  # 将符合条件的id添加到列表中
          except json.JSONDecodeError:
            pass
  return valid_ids  # 在函数结束时返回列表


print('欢迎大家关注我的推特：@CnzIvan，祝大家发财！仅供参考，不保证100%正确')
while True:
  address = input("请输入你的 ETH 地址: ")
  response = checkAddress(address)
  if response:
    if response.json() == []:
      print("该地址没有有效的数据。")
    else:
      valid_ids = checkResponse(response)  # 获取所有符合条件的id
      valid_ids.sort()  # 对列表进行排序
      result="符合条件的 id：\n"
      rcount=0
      for id in valid_ids:  # 打印所有符合条件的id
        rcount=rcount + 1
        result=result + str(id) + " " 
        
      print(result)
    print('逛逛告诉你你的记录数:'+ str(rcount))
  else:
    print("错误：无法获取到有效的响应。")
