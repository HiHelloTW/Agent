import json
from actions._utils import *
import importlib.util

class CreateNewAction(Action):
    PROMPT_TEMPLATE: str = """
    Please, based on the requirements enclosed by instruction {step}  in << >> below, provide a prompt that can solve the following problem, and ensure it adheres to the five points listed below.
    <<
    instruction:
    {instruction}
    >>
    
    1. Please refer only to **instruction {step}**.
    
    2. Following the step 1, Exclude everything from other instruction.

    3. Following the step 2, generate a JSON format only need JSON data:
    prompt:  "", // The full generated prompt
    name: "", // A short name for the prompt, following Python's naming convention.
    class_name: "" // A short name for the prompt, following Python's class name naming convention.
    
    4. Make sure the answer is only JSON
    
    5. Ensure the JSON format is correct
    """

    name: str = "CreateNewAction"

    async def run(self, instruction: str, step: int, action_history:list[str]):
        rsp = await self._aask(self.PROMPT_TEMPLATE.format(instruction=instruction, step=step))
        return generate_new_action(*extract_prompt_name(rsp))
        
    
        
import os

def extract_prompt_name(response: str):
    # 使用正則表達式擷取 JSON 內容
    match = re.search(r"(\{.*\})", response, re.DOTALL)
    if not match:
        return None
    
    json_str = match.group(1)
    
    try:
        data = json.loads(json_str)
        return data.get("prompt"), data.get("name"), data.get("class_name")
    except json.JSONDecodeError:
        return None
    
def generate_new_action(prompt, name, class_name):
    code = f'''from actions._utils import * 

class {class_name}(Action):
    PROMPT_TEMPLATE: str = """ 
    If Action history contains content, follow the Action history in the <<>> and {prompt}; otherwise, just {prompt}.

    <<Action history:
    {{action_history}}.
    >>
    """

    name: str = "{class_name}"

    async def run(self, instruction: str, step: int, action_history:list[str]):
        prompt = self.PROMPT_TEMPLATE.format(action_history=action_history)

        rsp = await self._aask(prompt)
        
        return rsp'''
    if name:
        # 建立 Python 檔案路徑
        file_path = os.path.join(os.getcwd(), "actions", f"{name}.py")

        # 寫入檔案
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)

        # 動態載入剛剛寫好的 module
        spec = importlib.util.spec_from_file_location(name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 取出 class，並回傳
        cls = getattr(module, class_name)

        # ✅ 產生 instance，並回傳
        instance: Action = cls()
        return instance

    else:
        raise ValueError("Parameter 'name' is required to save the file.")