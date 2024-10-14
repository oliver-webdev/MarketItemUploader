import requests
import json

def get_item():
    headers = {'Authorization': '3u5SZQRNH6Pbrp82AElirj'}
    url = 'https://api.commerce.naver.com/external/v2/products/channel-products/9311006387'
    
    res = requests.get(url=url, headers=headers)
    res_data = res.json()

    print(res_data)
    print(res_data.get('originProduct').get('statusType'))

    # output_file = "get_item.json"
    # with open(output_file, "w", encoding="utf-8") as f:
    #     json.dump(res_data, f, indent=4, ensure_ascii=False)

get_item()
