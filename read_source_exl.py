# read_source_exl.py

import pandas as pd

def read_excel_data(file_path):
    """
    엑셀 파일을 읽고 각 항목 값을 변수에 저장합니다.

    Parameters:
        file_path (str): 엑셀 파일 경로

    Returns:
        list: 각 행의 데이터를 담은 딕셔너리 리스트
    """
    df = pd.read_excel(file_path)

    data_list = []

    for index, row in df.iterrows():
        # if index == 0:
        #     # 제목행은 건너뜁니다.
        #     continue

        amazon_url = row['Amazon URL']
        # naver_tag_code = row['네이버태그코드']
        # naver_tag_text = row['네이버태그텍스트']
        # naver_meta_info = row['네이버메타정보']
        # product_property = row['제품속성']
        # product_property_value = row['제품속성값']

        # 각 행의 데이터를 딕셔너리로 저장
        data = {
            'amazon_url': amazon_url,
            # 'naver_tag_code': naver_tag_code,
            # 'naver_tag_text': naver_tag_text,
            # 'naver_meta_info': naver_meta_info,
            # 'product_property': product_property,
            # 'product_property_value': product_property_value
        }

        data_list.append(data)

    return data_list
