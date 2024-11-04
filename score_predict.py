import json
import openai

# 设置OpenAI API密钥
openai.api_key = "你的OpenAI API密钥"


from zhipuai import ZhipuAI
client = ZhipuAI(api_key="c1a70a187972b988ece0deb79be8ca0f.E5Bd5ODqZb7ozak0") # 请填写您自己的APIKey

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_all_answers(correct_answers, given_answers):
    prompt = """请比较以下正确答案和给出的答案，只考虑文字是否正确，忽略数字和标点符号。给出每个答案是否正确（正确/错误）的列表，对于多出来的字符则不考虑，视为正确。\n\n
    如：
    学生答案：'烘托出一片安静而☰和平的夜'，正确答案：'烘托出一片安静而和平的夜'，则视为正确。
    学生答案：'山岛辣特竦峙'，正确答案：'山岛竦峙'，仍视为正确。
    回答中只有正确/错误的列表，不需要其他文字：
    示例：
    1.正确
    2.错误
    3.正确
    """
    
    prompt += "正确答案：" + str(correct_answers) + "\n学生的答案：" + str(given_answers)
    


    completion = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": "你是一个严格的阅卷助手，负责比较答案是否正确。"},
                    {"role": "user", "content": prompt}
                ]
            )

    result = completion.choices[0].message.content




    return [line.strip().endswith("正确") for line in result.split("\n") if line.strip()]

def calculate_score(answers, results):
    correct_answers = answers['text_results']
    given_answers = results['text_results']
    
    comparison_results = compare_all_answers(correct_answers, given_answers)
    return sum(comparison_results)

def predict_score():
    # 加载JSON文件
    answers = load_json('ocr_anwser.json')
    results = load_json('ocr_results.json')

    # 计算分数
    total_score = calculate_score(answers, results)

    # 输出结果
    print(f"最终得分: {total_score}分 (满分6分)")

    return total_score

if __name__ == "__main__":
    predict_score()
