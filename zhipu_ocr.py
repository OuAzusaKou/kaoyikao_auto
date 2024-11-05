from zhipuai import ZhipuAI
import base64
import time

def zhipu_ocr_perform(image_path, client, max_retries=3, retry_delay=1):
    # 读取图片并转换为base64
    with open(image_path, "rb") as image_file:
        img_base = base64.b64encode(image_file.read()).decode('utf-8')
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="glm-4v",
                messages=[
                {
                    "role": "user",
                    "content": [
                    {
                        "type": "text",
                        "text": "请对图中文字进行OCR识别，不需要其他解释文字。"
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
                top_p=0.7,
                temperature=0.95,
                max_tokens=1024,
                stream=False
            )
            return response.choices[0].message.content
            
        except Exception as e:
            if attempt < max_retries - 1:  # 如果不是最后一次尝试
                print(f"OCR识别失败，正在进行第{attempt + 2}次尝试...")
                time.sleep(retry_delay)  # 等待一段时间后重试
                continue
            else:
                print(f"OCR识别最终失败: {str(e)}")
                return "OCR识别失败"  # 返回错误信息


if __name__ == "__main__":
    img_path = "screenshot copy.png"

    client = ZhipuAI(api_key="c1a70a187972b988ece0deb79be8ca0f.E5Bd5ODqZb7ozak0") # 填写您自己的APIKey

    print(zhipu_ocr_perform(img_path,client))
