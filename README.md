[![Watch the video](assets\images\favicon\gpt.webp)](https://youtu.be/Y7UkBZzChEs)

# 유튜브 실시간 채팅 자동 입력기 및 번역기 만들기

이번 블로그에서는 유튜브 실시간 채팅을 자동으로 복사하고 입력하는 프로그램을 만드는 방법과, 채팅 메시지를 자동으로 번역하는 방법을 소개하려고 한다. 이 프로그램은 `pytchat`, `pyautogui`, `pyperclip`, `openai` 라이브러리를 활용해 간단하게 구현할 수 있다.

## 준비물
- Python 3
- `pytchat`, `pyautogui`, `pyperclip`, `openai` 라이브러리 설치

```bash
pip install pytchat pyautogui pyperclip openai
```

## 코드 설명

아래는 전체 코드이다. 유튜브 채팅창의 메시지를 실시간으로 가져와서 특정 위치에 자동으로 입력해주고, GPT-4를 이용해 메시지를 번역해주는 기능을 한다.

```python
import pytchat
import pyautogui
import pyperclip
import openai

# 유튜브 채팅창의 주소 끝자리(=1&v= 표시 뒷부분)
video_id = "유튜브_채팅창의_주소_끝자리"

# 마우스 포인터 위치(입력할 채팅창)
mouse_coursor_x = 1535
mouse_coursor_y = 567

# OpenAI API 키 설정
openai.api_key = 'YOUR_API_KEY'

def translate_message(message, target_language="en"):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Translate the following message to english.."},
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
```

### 코드 분석

1. **라이브러리 임포트**
    ```python
    import pytchat
    import pyautogui
    import pyperclip
    import openai
    ```

    - `pytchat`: 유튜브 실시간 채팅을 가져오는 라이브러리
    - `pyautogui`: 마우스 및 키보드 자동화를 위한 라이브러리
    - `pyperclip`: 클립보드에 텍스트를 복사하기 위한 라이브러리
    - `openai`: OpenAI API를 이용해 GPT 모델을 사용하는 라이브러리

2. **유튜브 비디오 ID 설정**
    ```python
    video_id = "유튜브_채팅창의_주소_끝자리"
    ```
    유튜브 채팅창의 주소 끝부분에 있는 비디오 ID를 설정한다.

3. **마우스 포인터 위치 설정**
    ```python
    mouse_coursor_x = 1535
    mouse_coursor_y = 567
    ```
    채팅창에 입력할 위치의 마우스 좌표를 설정한다.

4. **OpenAI API 키 설정**

    ```python
    openai.api_key = 'YOUR_API_KEY'
    ```
    - OpenAI API 키를 설정한다. (본인의 API 키를 사용해야 한다.)
    - OpenAI API 키는 openai 사이트에 들어가서 회원가입을 하고 생성해야 한다. 처음 가입시 무료 사용량이 있는데 무료 기간이 지났거나 사용량이 초과했을때는 비용을 지불해야 한다.
    - 직접 AI서버를 구축하는 것보다 건당 사용료를 내는 것이 훨씬 효율적이다. 괜히 해본다고 비싼 그래픽카드 사지말고, API를 어떻게 이용할 것인가만 생각하자. **AI인프라는 개인이 감당할 수 있는 비용이 아니다.**

5. **메시지 번역 함수**
    ```python
    def translate_message(message, target_language="ko"):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Translate the following message to english"},
                {"role": "user", "content": message}
            ],
            max_tokens=100
        )
        translation = response['choices'][0]['message']['content']
        return translation
    ```
    - `translate_message`: 입력된 메시지를 지정된 언어로 번역하는 함수이다. 기본 언어는 영어로 설정되어 있다.
    - GPT-4 모델을 사용하여 번역을 수행한다.

6. **채팅 객체 생성 및 메시지 처리**
    ```python
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
    ```
    - `pytchat.create(video_id)`: 유튜브 채팅 객체를 생성한다.
    - `while chat.is_alive()`: 채팅이 활성화된 동안 반복한다.
    - `for c in chat.get().sync_items()`: 실시간으로 채팅 메시지를 가져온다.
    - 원본 메시지를 가져와서 길이가 99자를 넘으면 건너뛴다.
    - 메시지를 번역한 후, 클립보드에 복사하고 마우스 포인터를 이동시켜 클릭하여 채팅창에 붙여넣기 및 전송을 수행한다.

### 주의사항
- 마우스 좌표는 화면 해상도와 배율에 따라 달라질 수 있으므로, 자신의 환경에 맞게 조정해야 한다.
- 많은 양의 채팅입력시 일부만 처리하는 현상이 나타난다. api를 통해 번역이 진행되기 때문에 네트워크 지연발생 및 답변을 생성하는 시간이 있기 때문에 느리다.
- OpenAI API 사용 시 발생할 수 있는 비용에 유의해야 한다.

이 코드를 통해 유튜브 실시간 채팅을 보다 효율적으로 관리하고, 자동으로 번역된 메시지를 입력할 수 있다. 다양한 활용 사례를 생각해보고, 필요한 부분을 수정하여 더 유용하게 사용해보자.
