from openai import OpenAI

def make_ai_message(system_prompt: str, human_message: str) -> str:
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_message},
        ],
    )
    ai_message = completion.choices[0].message.content
    return ai_message