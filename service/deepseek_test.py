import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

english_word = "insert"

messages = [
    {
        "role": "user",
        "content": f"""Please provide the following about the English word "{english_word}" in the format below:

1. 意味（日本語で簡潔に）
2. 例文（小学生でも理解できる自然な英語文）
3. 和訳（例文の日本語訳）

Format:
1. 意味: ...
2. 例文: ...
3. 和訳: ...
"""
    }
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)

full_text = response.choices[0].message.content.strip()

# 正規表現で抽出
meaning_match = re.search(r"1\. 意味:\s*(.*)", full_text)
example_match = re.search(r"2\. 例文:\s*(.*)", full_text)
translation_match = re.search(r"3\. 和訳:\s*(.*)", full_text)

meaning = meaning_match.group(1).strip() if meaning_match else "Not found"
example_sentence = example_match.group(1).strip() if example_match else "Not found"
translation = translation_match.group(1).strip() if translation_match else "Not found"

# 結果を表示
print("📘 意味:", meaning)
print("📝 例文:", example_sentence)
print("🌸 和訳:", translation)
