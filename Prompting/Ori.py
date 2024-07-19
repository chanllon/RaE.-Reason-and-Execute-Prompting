# -*- coding:utf-8 -*-
import PALMGeo
# from PALMGeo.prompt import geometry_cot
import re
import os

import google.generativeai as genai
import PIL.Image
import threading


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




def GPT4(image_path,question):
  interface = PALMGeo.interface.ProgramChatInterface(
    # model='gpt-3.5-turbo-instruct',
    model='gpt-4-vision-preview',
    stop='\n\n\n', # stop generation str for Codex API
    get_answer_expr='solution()' # python expression evaluated after generated code to obtain answer
  )
  # image_path='img_diagram_point.png'
  # question = 'Find x.'
  Mode='gpt-4-vision-preview'
  # prompt = geometry_cot.Geometry_Prompt.format(question=question)
  answer = interface.run(Mode,image_path,question)
  # print(answer)
  return answer


def Qwenplus(image_path,question):
  # prompt = geometry_cot.Geometry_Prompt.format(question=question)
  interface = PALMGeo.interface.ProgramChatInterface(
    # model='gpt-3.5-turbo-instruct',
    model='qwen-vl-plus',
    stop='\n\n\n', # stop generation str for Codex API
    get_answer_expr='solution()' # python expression evaluated after generated code to obtain answer
  )
  model='qwen-vl-plus'
  answer = interface.run(model,image_path, question)
  print(answer)
  return answer


def Gemin(image_path,question):
  # prompt = geometry_cot.Geometry_Prompt.format(question=question)
  interface = PALMGeo.interface.ProgramChatInterface(
    # model='gpt-3.5-turbo-instruct',
    model='gemini-pro-vision',
    stop='\n\n\n',  # stop generation str for Codex API
    get_answer_expr='solution()'  # python expression evaluated after generated code to obtain answer
  )
  model = 'gemini-pro-vision'
  answer = interface.run(model, image_path, question)
  print(answer)
  return answer