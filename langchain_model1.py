import requests
import json
import os
from bs4 import BeautifulSoup

level = 'Medium'
problem_num = '0180-consecutive-numbers'
# input leetcode data
git_md = f'https://raw.githubusercontent.com/poriz/leetcode/main/LeetCode/{level}/{problem_num}/README.md'
res = requests.get(git_md)
description = BeautifulSoup(res.content, 'html.parser')

solved_codes = f'https://raw.githubusercontent.com/poriz/leetcode/main/LeetCode/{level}/{problem_num}/{problem_num}.sql'
res = requests.get(solved_codes)
my_code = BeautifulSoup(res.content, 'html.parser')

# Ollama API 서버의 URL
url = 'http://localhost:11434/api/generate'

# 요청에 사용할 데이터
data = {
    "model": "qwen2",
    "prompt":
        f"""
        I want markdown file to make blog posts. blog language is korean!!!
        Tell me the table and examples, but other than that, write them down like a blog
        

        first make description about problem. 
        here is description. 
        {description}

        Second, show my SQL code useing codeblock 
        here is my code. 
        {my_code}

        finally evaluate my code
        And if you have better code, please explain it additionaly

        """
    }

# HTTP POST 요청 보내기 (스트리밍 응답 받기)
response = requests.post(url, json=data, stream=True)

# 응답 본문을 한 줄씩 처리
translated_text = ""

try:
    for line in response.iter_lines():
        if line:
            # 각 줄을 JSON으로 파싱
            line_data = json.loads(line.decode('utf-8'))
            # 응답에서 'response' 키의 값을 추가
            translated_text += line_data.get('response', '')
except json.JSONDecodeError as e:
    print("JSON decode error:", e)

# 완성된 번역된 텍스트 출력
print('fin')

file_path = './mdfile.md'
with open (file_path,'w') as file_data:
    file_data.write(translated_text)


