import json
import openai

# 设置OpenAI API密钥
openai.api_key = "你的OpenAI API密钥"

from zhipuai import ZhipuAI

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_characters_presence(standard_answers, student_answer):
    """
    检查标准答案列表中的每个答案的字符是否都出现在学生答案中
    
    Args:
        standard_answers: 标准答案字符串列表
        student_answer: 学生答案字符串
    
    Returns:
        包含True/False的列表，表示每个标准答案是否正确
    """
    results = []
    for standard in standard_answers:
        # 移除所有空格和标点符号
        cleaned_standard = ''.join(char for char in standard if char.isalnum())
        cleaned_answer = ''.join(char for char in student_answer if char.isalnum())
        
        # 检查标准答案的每个字符是否都在学生答案中
        is_correct = all(char in cleaned_answer for char in cleaned_standard)
        results.append(is_correct)
    
    return results

def compare_all_answers(correct_answers, given_answers, client):
    # 修改比较逻辑，使用新的字符检查函数
    given_answers_0 = ' '.join(given_answers[0])
    given_answers_1 = given_answers[1]
    combined_answer = given_answers_0 +  ' ' + given_answers_1 # 合并两组答案
    results = check_characters_presence(correct_answers, combined_answer)
    
    # # 为了保持与原有代码兼容，我们仍然使用智谱AI进行验证
    # prompt = """请比较以下标准答案和给出的答案，只考虑文字是否正确，忽略数字和标点符号。给出每个答案是否正确（正确/错误）的列表，对于多出来的字符则不考虑，视为正确。\n\n
    # 如：
    # 学生答案：'烘托出一片安静而☰和平的夜'，标准答案：'烘托出一片安静而和平的夜'，则视为正确。
    # 学生答案：'山岛辣特竦峙'，标准答案：'山岛竦峙'，仍视为正确。
    # 注意学生会给出两组答案，只要两组答案中可以拼接出标准答案，则视为正确。
    # "标准答案"有几个，则返回的列表中就有几个。
    # 回答中只有正确/错误的列表，不需要其他文字：
    # 示例：
    # 1.正确
    # 2.错误
    # 3.正确
    # """
    
    # prompt += "正确答案：" + str(correct_answers) + "\n学生的答案：" + str(given_answers)
    


    # completion = client.chat.completions.create(
    #             model="glm-4-flash",
    #             messages=[
    #                 {"role": "system", "content": "你是一个严格的阅卷助手，负责比较答案是否正确。"},
    #                 {"role": "user", "content": prompt}
    #             ]
    #         )

    # result = completion.choices[0].message.content




    # return [line.strip().endswith("正确") for line in result.split("\n") if line.strip()]
    return results

def calculate_score(answers, results, client):
    given_answers = []
    correct_answers = answers['text_results']
    given_answers.append(results['baidu_results'])
    given_answers.append(results['zhipu_results'])
    
    comparison_results = compare_all_answers(correct_answers, given_answers,client)

    # 将 True 转换为 1，False 转换为 0
    comparison_results = [1 if result else 0 for result in comparison_results]
    
    return sum(comparison_results)

def predict_score(client):
    # 加载JSON文件
    answers = load_json('ocr_anwser.json')
    results = load_json('ocr_results.json')

    # 计算分数
    total_score = calculate_score(answers, results,client)

    # 输出结果
    print(f"最终得分: {total_score}分 (满分6分)")

    return total_score

if __name__ == "__main__":

    client = ZhipuAI(api_key="c1a70a187972b988ece0deb79be8ca0f.E5Bd5ODqZb7ozak0") # 请填写您自己的APIKey

    predict_score(client)
