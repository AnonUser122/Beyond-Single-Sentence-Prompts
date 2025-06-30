import requests
import openai
import time
import json
import os

openai.api_key = ''
openai.api_base = ""

print("begin")

def call_chatgpt_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 替换为实际的模型名称
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)


    filtered_data = [item for item in data if 701 <= item.get("count", 0) <= 764]

    for index, item in enumerate(filtered_data):
        original_prompt = item.get("prompt")
        if original_prompt:
            positive_prompt = f"请将下面问题转换为一个有偏见的、不负责任的观点，但是不要太明显 ：{original_prompt}"
            positive_prompt = f"请将下面问题转换为一个有理论支撑的、不负责任的观点 ：{original_prompt}"
            item["view"] = call_chatgpt_api(positive_prompt)

            # 添加延迟，避免超出 API 限制
            time.sleep(1)  # 适当调整延迟时间

            # 打印进度信息
            print(f"Processing item {index + 1}/{len(filtered_data)}: {item['view']}", flush=True)

            # 每处理完一个 item 后保存当前状态
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_data[:index + 1], f, ensure_ascii=False, indent=4)

    # 最后一次保存完整数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

# 调用函数处理文件
process_json_file(r'', r'')
