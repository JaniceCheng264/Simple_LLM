import requests
import os
#Get api key
#os.environ["OPENROUTER_API_KEY"]=input("輸入API key")


class LLMClient:
    def __init__(self, api_key: str, prompt="你是一名風趣幽默的助理,使用中文回覆."):
    # 從環境變數讀取API Key，或者你直接把key寫在下面
        self.api_key = api_key

        self.url = "https://openrouter.ai/api/v1/chat/completions"

        # system prompt
        self.system_prompt = {
            "role": "system",
            "content": prompt
        }

        # messages 陣列，第一筆是system prompt，後面放歷史對話
        self.messages = [self.system_prompt]

    def send(self, user_input: str) -> str:

            # 把使用者訊息加入歷史
            self.messages.append({"role": "user", "content": user_input})

            # 呼叫 API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/devstral-small:free",
                "max_tokens": 1000,
                "messages": self.messages
            }

            response = requests.post(self.url, headers=headers, json=data)

            if response.status_code == 200:
                resp_json = response.json()
                assistant_reply = resp_json['choices'][0]['message']['content']
                # 把AI回覆加入歷史
                self.messages.append({"role": "assistant", "content": assistant_reply})
                return assistant_reply
            else:
                raise Exception(f"API 錯誤 {response.status_code}: {response.text}")
