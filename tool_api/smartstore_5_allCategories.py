import requests
import json

def get_all_categories():
    from datetime import datetime, timedelta

    headers = {'Authorization': '6l4GMxoAjgNZrhh6laTZOl'}
    url = 'https://api.commerce.naver.com/external/v1/categories'
    
    res = requests.get(url=url, headers=headers)
    res_data = res.json()
    
    output_file = "output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(res_data, f, indent=4, ensure_ascii=False)

get_all_categories()
