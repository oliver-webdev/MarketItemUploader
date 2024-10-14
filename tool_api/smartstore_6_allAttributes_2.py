import requests
import json

def get_all_categories():
    from datetime import datetime, timedelta

    headers = {'Authorization': 'RutGCbx12lNcEC8PFFd60'}
    url = 'https://api.commerce.naver.com/external/v1/product-attributes/attribute-values?categoryId=50000570'
    
    res = requests.get(url=url, headers=headers)
    res_data = res.json()


    # print(json.dumps(res_data, indent=4, ensure_ascii=False))
    
    output_file = "모든속성3.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(res_data, f, indent=4, ensure_ascii=False)

get_all_categories()
