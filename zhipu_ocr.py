from zhipuai import ZhipuAI
import base64
client = ZhipuAI(api_key="c1a70a187972b988ece0deb79be8ca0f.E5Bd5ODqZb7ozak0") # 填写您自己的APIKey




def zhipu_ocr_perform(img_path):
    with open(img_path, 'rb') as img_file:
        img_base = base64.b64encode(img_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="glm-4v",
        messages=[
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "请解析图中的文字"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url" : img_base
                }
            }
            ]
        }
        ],
        top_p= 0.7,
        temperature= 0.95,
        max_tokens=1024,
        stream=False
        )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    img_path = "screenshot copy.png"
    print(zhipu_ocr_perform(img_path))
