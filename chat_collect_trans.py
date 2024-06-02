import pytchat
import pyautogui
import pyperclip
import openai

# 유튜브 채팅창의 주소 끝자리(=1&v= 표시 뒷부분)
video_id = "your_youtube_video_id"

# 마우스 포인터 위치(입력할 채팅창)
mouse_coursor_x = 1535
mouse_coursor_y = 567

# OpenAI API 키 설정
openai.api_key = 'Your_api_key'

def translate_message(message, target_language="en"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Translate the following message to english."},
            {"role": "user", "content": message}
        ],
        max_tokens=100
    )
    translation = response['choices'][0]['message']['content']
    return translation

chat = pytchat.create(video_id)
while chat.is_alive():
    for c in chat.get().sync_items():
        original_message = f"[{c.author.name}]- {c.message}"
        if len(original_message) > 99:
            continue
        translated_message = translate_message(original_message)
        print(translated_message)
        pyperclip.copy(translated_message)
        pyautogui.moveTo(mouse_coursor_x, mouse_coursor_y)
        pyautogui.click()
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('return')