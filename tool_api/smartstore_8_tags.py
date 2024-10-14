import requests
import json

def search_tags():

    keyword = "피규어"
    headers = {'Authorization': '1kzukuAywRfZcG3qz38nQi'}
    url = f'https://api.commerce.naver.com/external/v2/tags/recommend-tags?keyword={keyword}'
    
    res = requests.get(url=url, headers=headers)
    res_data = res.json()

    # 콘솔에 출력
    print(json.dumps(res_data, indent=4, ensure_ascii=False))
    
    # 파일로 출력
    # output_file = "get_item.json"
    # with open(output_file, "w", encoding="utf-8") as f:
    #     json.dump(res_data, f, indent=4, ensure_ascii=False)

search_tags()
