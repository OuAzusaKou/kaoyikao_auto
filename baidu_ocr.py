# encoding:utf-8

import requests
import base64
import json

def extract_text(ocr_result):
    return [item['words'] for item in ocr_result['words_result']]

def perform_ocr(image_path):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
    
    # 二进制方式打开图片文件
    with open(image_path, 'rb') as f:
        img = base64.b64encode(f.read())
    
    params = {"image": img}
    access_token = '24.1dac46a55d7a80b115bb2ff88c43aca0.2592000.1733327277.282335-115752088'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        result = response.json()
        print(result)  # 打印原始结果
        
        # 提取文字结果
        text_results = extract_text(result)
        
        # 将文字结果保存到JSON文件
        output = {
            "baidu_results": text_results,
            "total_words": len(text_results)
        }
        
        with open('ocr_results.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        
        print("OCR结果已保存到 ocr_results.json 文件中")
    else:
        print("OCR识别失败")

if __name__ == "__main__":
    perform_ocr('screenshot copy.png')