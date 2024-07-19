# Copyright 2022 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import signal
import threading
import base64
from contextlib import redirect_stdout
from typing import Any, Callable, List, Optional
from collections import Counter

from .runtime import GenericRuntime
from .backend import call_gpt, call_chat_gpt,call_MM_gpt,call_MM_Qwen,call_MM_Gen


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


class TextInterface:
    
    def __init__(
        self,
        model: str = 'gpt-3.5-turbo-instruct',
        answer_prefix: str = 'The answer is:',
        stop: str = '\n\n\n',
        extract_answer: Optional[Callable[[str], Any]] = None,
    ):
        self.history = []
        self.answer_prefix = answer_prefix
        self.extract_answer_fn = extract_answer
        self.stop = stop
        self.model = model

    def clear_history(self):
        self.history = []

    def extract_answer(self, gen: str):
        if self.extract_answer_fn:
            return self.extract_answer_fn (gen)
        last_line = gen.strip().split('\n')[-1]
        return last_line[len(self.answer_prefix):].strip()

    def run(self, prompt, temperature=0.0, top_p=1.0, majority_at=None, max_tokens=512):
        gen = call_gpt(prompt, model=self.model, stop=self.stop,
            temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at)
        self.history.append(gen)
        return self.extract_answer(gen)


class ProgramInterface:

    def __init__(
        self,
        model: str = 'gpt-3.5-turbo',
        runtime: Optional[Any] = None,
        stop: str = '\n\n',
        get_answer_symbol: Optional[str] = None,
        get_answer_expr: Optional[str] = None,
        get_answer_from_stdout: bool = False,
        verbose: bool = False
    ) -> None:

        self.model = model
        self.runtime = runtime if runtime else GenericRuntime()
        self.history = []
        self.stop = stop
        self.answer_symbol = get_answer_symbol
        self.answer_expr = get_answer_expr
        self.get_answer_from_stdout = get_answer_from_stdout
        self.verbose = verbose
        
    def clear_history(self):
        self.history = []
    
    def process_generation_to_code(self, gens: str):
        return [g.split('\n') for g in gens]
    
    def generate(self, prompt: str, temperature: float =0.0, top_p: float =1.0, 
            max_tokens: int =512, majority_at: int =None, ):
        gens = call_gpt(prompt, model=self.model, stop=self.stop, 
            temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at, )
        if self.verbose:
            print(gens)
        code = self.process_generation_to_code(gens)
        self.history.append(gens)
        return code
    
    def execute(self, code: Optional[List[str]] = None):
        code = code if code else self.code
        if self.get_answer_from_stdout:
            program_io = io.StringIO()
            with redirect_stdout(program_io):
                self.runtime.exec_code('\n'.join(code))
            program_io.seek(0)
            return program_io.readlines()[-1]
        elif self.answer_symbol:
            self.runtime.exec_code('\n'.join(code))
            return self.runtime._global_vars[self.answer_symbol]
        elif self.answer_expr:
            self.runtime.exec_code('\n'.join(code))
            return self.runtime.eval_code(self.answer_expr)
        else:
            self.runtime.exec_code('\n'.join(code[:-1]))
            return self.runtime.eval_code(code[-1])
    
    def run(self, prompt: str, time_out: float =10, temperature: float =0.0, top_p: float =1.0, 
            max_tokens: int =512, majority_at: int =None):
        code_snippets = self.generate(prompt, majority_at=majority_at, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        
        results = []
        for code in code_snippets:
            with timeout(time_out):
                try:
                    exec_result = self.execute(code)
                except Exception as e:
                    print(e)
                    continue
                results.append(exec_result)
        
        if len(results) == 0:
            print('No results was produced. A common reason is that the generated code snippet is not valid or did not return any results.')
            return None
        
        counter = Counter(results)
        return counter.most_common(1)[0][0]
    
    
SYSTEM_MESSAGES = 'You are a helpful python programmer.'
class ProgramChatInterface(ProgramInterface):
    def __init__(self, *args, system_message: str = SYSTEM_MESSAGES, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_message = system_message

    # Function to encode the image
    def encode_image(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate(self, prompt: str, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        messages =[ {'role': 'user', 'content': prompt}]
        # print(messages)
        gen = call_chat_gpt(messages, model=self.model, stop=self.stop, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        if self.verbose:
            print(gen)
        self.history.append(gen)
        return self.process_generation_to_code(gen)

    def generate_IQ(self, sys:str, image:str,prompt: str, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        base64_image = self.encode_image(image)
        messages =[{'role': 'system', 'content': sys},
                   {"role": "user","content": [{"type": "text","text": prompt },{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}" } }] }]

        # print(messages)
        gen = call_MM_gpt(messages, model=self.model, stop=self.stop, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        if self.verbose:
            print(gen)
        self.history.append(gen)
        codespli=self.process_generation_to_code(gen)
        return codespli

    def generate_Qwen(self, image:str,prompt: str, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        # base64_image = self.encode_image(image)
        # print('qqqq')
        gen=call_MM_Qwen(prompt,image)
        if self.verbose:
            print(gen)
        self.history.append(gen)
        codespli=self.process_generation_to_code(gen)
        return codespli

    def generate_Gen(self, image:str,prompt: str, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        # base64_image = self.encode_image(image)
        # print('qqqq')
        gen=call_MM_Gen(image,prompt)
        if self.verbose:
            print(gen)
        self.history.append(gen)
        codespli=self.process_generation_to_code(gen)
        return codespli

    def process_generation_to_code(self, gens: str):
        # print(gens)
        if '```python' in gens:
            gens = gens.split('```python')[1].split('```')[0]
        elif '```' in gens:
            gens = gens.split('```')[1].split('```')[0]
        elif '# solution in Python:' in gens:
            gens= gens.split('# solution in Python:')[1].split('# Call the function and print the result')[0]
        else:
            gens=None
        print('',gens)
        # with open('RaE_2.txt', 'a',encoding='utf-8') as file:
        #     file.write(gens+'\n')
        return gens.split('\n')
    
    def run(self, Mode, image: str, prompt: str, time_out: float = 10, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        # code = self.generate(prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        if Mode=='gpt-4-vision-preview':
            sys='You are a useful assistant who can use relevant domain knowledge to reason " #reasoning:" and write Python code "def solution():" to solve geometric problems, similar to the examples provided.'
            codesplit = self.generate_IQ(sys,image,prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        elif Mode=='qwen-vl-plus':
            codesplit=self.generate_Qwen(image,prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        elif Mode=='gemini-pro-vision':
            codesplit=self.generate_Gen(image,prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        else:
            print('')
        exec_result='init'
        if codesplit==None:
            return exec_result
        else:
            with timeout(time_out):
                try:
                    exec_result = self.execute(codesplit)
                except Exception as e:
                    print(e)

            return exec_result
