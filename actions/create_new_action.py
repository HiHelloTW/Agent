import json
from actions.utils import *
import importlib.util

class CreateNewAction(Action):
    PROMPT_TEMPLATE: str = """
    Please, based on the requirements enclosed in << >> below, provide a prompt that can solve the following problem, and ensure it adheres to the five points listed below.
    <<{instruction}>>
    
    1. Ignore the subject in the text.
    
    2. Following the step 1, Use the remaining content to generate a prompt to process the content.

    3. Following the step 2, generate a JSON format only need JSON data:
    prompt:  "", // The full generated prompt
    name: "", // A short name for the prompt, following Python's naming convention.
    class_name: "" // A short name for the prompt, following Python's class name naming convention.
    
    4. Make sure the answer is only JSON
    
    5. Ensure the JSON format is correct
    """

    name: str = "CreateNewAction"

    async def run(self, instruction: str):
        rsp = await self._aask(self.PROMPT_TEMPLATE.format(instruction=instruction))
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
    code = f'''from actions.utils import * 

class {class_name}(Action):
    PROMPT_TEMPLATE: str = """
    {{instruction}}.
    {prompt}
    """

    name: str = "{class_name}"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

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