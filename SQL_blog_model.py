import requests
import json
import os

# Ollama API 서버의 URL
url = 'http://localhost:11434/api/generate'

# 요청에 사용할 데이터
data = {
    "model": "llama3",
    "prompt":
        """Do not write answers other than the contents of the md file.
        1. Want an md file answer for blogging.
        2. The subject of the blog post is Airflow.
        3. The target of the blog post is those who start studying.
        4. Please attach the appropriate example code together
        5. If necessary, please include a reference
        6. Please include a little bit of detail to match the tech blog. Please also include examples of details.
        7. If you can put a picture of the explanation, please put it in
        8. lastly translate korean"""
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


