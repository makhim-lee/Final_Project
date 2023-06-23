import openai

openai.api_key = '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'  # OpenAI API 키를 입력하세요

def infer_location(object_list):
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]

    user_input = "다음 물건들이 있는 장소가 어딘지 유추해줘"
    object_list_str = ", ".join(object_list)
    message = f"{user_input} {object_list_str}"

    messages.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message

    print("Assistant:", reply.content)

    messages.append(reply)

# 사용자가 입력한 사물 리스트
object_list = input("사물 리스트를 입력하세요 (쉼표로 구분): ").split(",")

infer_location(object_list)
