import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수 가져오기
key = os.getenv("OPENAI_API_KEY")

def print_prices(input_tokens: int, output_tokens: int) -> None:
    input_price = (input_tokens * 0.150 / 1_000_000) * 1_500
    output_price = (output_tokens * 0.600 / 1_000_000) * 1_500
    print("input: tokens {}, krw {:.4f}".format(input_tokens, input_price))
    print("output: tokens {}, krw {:4f}".format(output_tokens, output_price))


def make_ai_message(question: str) -> str:
    client = openai.Client(api_key=key)  # 명시적으로 키 지정

    res = client.chat.completions.create(
        messages=[
            { "role": "user", "content": question },
        ],
        model="gpt-4o-mini",
        temperature=0.3, # 창의성
    )
    # prompt_tokens : 입력 토큰 수
    # completion_tokens : 출력 토큰 수
    print_prices(res.usage.prompt_tokens, res.usage.completion_tokens)
    return res.choices[0].message.content


def main():
    지식 = open("backdabang.txt", "rt", encoding="utf-8").read()

    question = f"""넌 AI Assistant. 모르는 건 모른다고 대답.

[[빽다방 메뉴 정보]]
{지식}

질문: 빽다방 카페인이 높은 음료와 가격은?"""
    ai_message = make_ai_message(question)
    print(ai_message)


if __name__ == "__main__":
    main()