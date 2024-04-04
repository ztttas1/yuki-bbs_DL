import requests
import re
import os
from datetime import datetime

def clean_text(text):
    """HTMLタグやその他不要な文字列を除去する"""
    if text:
        cleaned_text = re.sub(r'<.*?>', '', text)
        return cleaned_text
    return text

def extract_name_message(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 現在の日時を取得し、ファイル名に使用する形式に変換
        now = datetime.now()
        file_name = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
        directory = "bbs"
        file_path = os.path.join(directory, file_name)

        # bbsディレクトリが存在するか確認し、存在しなければ作成
        if not os.path.exists(directory):
            os.makedirs(directory)

        lines = []

        if 'contents' in data:
            for item in data['contents']:
                name = item.get('name')
                message = item.get('message')

                cleaned_name = clean_text(name)
                cleaned_message = clean_text(message)

                new_content = f"Name: {cleaned_name}\nMessage: {cleaned_message}\n\n"
                lines.append(new_content)

        # 更新された内容をファイルに書き込み
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 使用例
url = "https://yukibbs-server.onrender.com/dev/bbs/api?start=100"
extract_name_message(url)
