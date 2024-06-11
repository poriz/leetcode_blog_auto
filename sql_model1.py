import requests
import json
import os
from bs4 import BeautifulSoup
import re

def get_latest_commit_sha(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    params = {'per_page': 1}  # 최근 커밋 하나만 가져오기 위한 파라미터

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 요청 오류 확인

        commit_data = response.json()[0]
        sha = commit_data['sha']
        return sha
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return None
    
def get_latest_commit_file(repo_owner, repo_name):
    latest_sha = get_latest_commit_sha(repo_owner, repo_name)
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{latest_sha}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 요청 오류 확인

        commit_data = response.json()
        files = commit_data['files']
        if files:
            latest_file_name = files[0]['filename']
            return latest_file_name
        else:
            return None  # 커밋에 파일이 없는 경우
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API - sha: {e}")
        return None

owner = 'poriz'
repo_name = 'leetcode'
latest_file = get_latest_commit_file(owner,repo_name)
# 예시: 'owner'와 'repo_name'을 실제 레포지토리의 소유자와 이름으로 변경해야 합니다.

level = re.search(r'LeetCode/(.*?)/', latest_file).group(1)
pattern = rf'{level}\/(.*?)\/'
problem_num = re.search(pattern, latest_file).group(1)

# warning!!
token = 'your_git_token'
headers = {'Authorization': 'token ' + token}
# warning!!
# input leetcode data
git_md = f'https://raw.githubusercontent.com/{owner}/leetcode/main/LeetCode/{level}/{problem_num}/README.md'
res = requests.get(git_md,headers=headers)
description = BeautifulSoup(res.content, 'html.parser')

solved_codes = f'https://raw.githubusercontent.com/{owner}/leetcode/main/LeetCode/{level}/{problem_num}/{problem_num}.sql'
res = requests.get(solved_codes,headers=headers)
my_code = BeautifulSoup(res.content, 'html.parser')


# Ollama API 서버의 URL
url = 'http://localhost:11434/api/generate'

# 요청에 사용할 데이터
data = {
    "model": "qwen2",
    "prompt":
        f"""
        내가 진행한 리트코드의 문제풀이에 대해서 블로그 글을 작성하려고 한다.
        utf-8으로 인코딩하고!! 블로그의 모든 내용은 한글로 작성한다. 
        결과는 markdown 형식으로 결과를 출력해주어야 한다.
        
        블로그에 들어갈 말 이외에 답변은 하지 않게 해줘.

        블로그의 구성은 다음과 같다.
        제목에는 문제번호를 적어라

        그리고 내용에는 다음과 같이 구성해라.

        1. **문제와 테이블**
        - description: {description} 
        - description 을 참고해서 글을 작성해야한다.

        - 문제: 해당 문제의 내용을 영문과 한글번역 모두 보여준다.
        - 테이블 & 예제: 문제의 테이블과 예제를 자세하게 보여준다. 
        - 예제는 discription의 'Example 1'의 내용을 가져와 작성한다.

        2. **풀이 및 피드백**
        - 풀이: 나의 풀이를 작성 및 설명한다. 이때 내 코드는 변경하지 말아야 한다.
        - 피드백: 나의 풀이의 개선점에 대해서 피드백한다.
        - 내 코드: {my_code}
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

file_path = './mdfile2.md'
with open (file_path,'w') as file_data:
    file_data.write(translated_text)


