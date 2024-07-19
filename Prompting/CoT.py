# -*- coding:utf-8 -*-
import PALMGeo
from PALMGeo.prompt import geometry_cot
import threading
import requests
import base64
import re
import time
import dashscope
import google.generativeai as genai
import PIL.Image
import openai

dashscope.api_key=''
openai.api_key = ''

class timeout:
  def __init__(self, seconds=1, error_message='Timeout'):
    self.seconds = seconds
    self.error_message = error_message

  def timeout_handler(self, signum, frame):
    raise TimeoutError(self.error_message)

  def __enter__(self):
    # signal.signal(signal.SIGALRM, self.timeout_handler)
    # signal.alarm(self.seconds)
    self.timer = threading.Timer(self.seconds, self.timeout_handler)
    self.timer.start()

  def __exit__(self, type, value, traceback):
    # signal.alarm(0)
    if self.timer:
      self.timer.cancel()

# os.environ["http_proxy"] = "http://127.0.0.1:21882"                # 指定代理，解决连接问题
# os.environ["https_proxy"] = "http://127.0.0.1:21882"


def gpt_4_vision(image_path, text):
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
  }
  wait = 1
  while True:
    try:
      with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
      payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": text,
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 3000
      }
      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      res = response.json()
      with open('gpt_4OutPut.txt', 'a', encoding='utf-8') as file:
        file.write('answer:' + str(res['choices'][0]['message']['content']) + '\n')
      return re.search(r'\d+(\.\d+)?(?=\D*$)', res['choices'][0]['message']['content']).group(0)
    except openai.APIError as e:
      time.sleep(min(wait, 2))
      wait *= 2
    raise RuntimeError('Failed to call chat gpt')
def Qwenplus(img, question):
  wait = 1
  while True:
    try:
      dashscope.api_key = ''
      local_file_path = 'file://' + img
      messages = [
        {
          'role': 'system',
          'content': [{
            'text': 'You are a useful assistant who can use relevant domain knowledge to reason " #reasoning:" and write Python code "def solution():" to solve geometric problems, similar to the examples provided.'
          }]
        },
        {
          "role": "user",
          "content": [
            {"image": local_file_path},
            {"text": question},
            # {"text": "After all the queries are run and you get the answer, put the answer in \\boxed{}"}
          ]
        }
      ]
      response = dashscope.MultiModalConversation.call(model='qwen-vl-plus', messages=messages)
      return re.search(r'\d+(\.\d+)?(?=\D*$)', response.output.choices[0].message.content[0]['text']).group(0)
    except OSError as e:
      time.sleep(min(wait, 2))
      wait *= 2
    raise RuntimeError('Failed to call chat gpt')
def Gemin(image_path, text):
  wait = 1
  while True:
    try:
      img = PIL.Image.open(image_path)
      genai.configure(api_key='')
      model = genai.GenerativeModel('gemini-pro-vision')
      response = model.generate_content(
        [text, img],
        generation_config=genai.types.GenerationConfig(
          # Only one candidate for now.
          candidate_count=1,
          stop_sequences=['x'],
          # max_output_tokens=1000,
          temperature=0))
      response.resolve()
      # print('模型回复：', response.text)
      return re.search(r'\d+(\.\d+)?(?=\D*$)', response.text).group(0)
    except OSError as e:
      time.sleep(min(wait, 2))
      wait *= 2
    raise RuntimeError('Failed to call chat gpt')

def GPT4CoT(image_path,question):
  prompt = geometry_cot.Geometry_Prompt.format(question=question)
  answer=gpt_4_vision(image_path,prompt)
  print('回答：',answer)
  return answer


def QwenplusCoT(image_path,question):
  prompt = geometry_cot.Geometry_Prompt.format(question=question)
  answer = Qwenplus(image_path, prompt)
  # print(answer)
  return answer


def GeminCoT(image_path,question):
  prompt = geometry_cot.Geometry_Prompt.format(question=question)
  answer = Gemin(image_path, prompt)
  # print(answer)
  return answer