import json
from actions.actionsImport import *

class CreateNewAction(Action):
    PROMPT_TEMPLATE: str = """
    Please carefully read the following content requirements and generate a response based on them:  
    ""{instruction}""

    Please compose a complete response according to the above requirements. Be sure to follow these two points:  
    1. Response must include the following two parts:  
   - prompt: Generated complete prompt
   - name: A short name for the prompt without space
    """

    name: str = "CreateNewAction"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        prompt, name = extract_prompt_name(rsp)
        
        generate_new_action(prompt, name)
        return
    
import os

def extract_prompt_name(response: str):
    # 使用正則表達式擷取 JSON 內容
    match = re.search(r"(\{.*\})", response, re.DOTALL)
    if not match:
        return None
    
    json_str = match.group(1)
    
    try:
        data = json.loads(json_str)
        return data.get("prompt"), data.get("name")
    except json.JSONDecodeError:
        return None
    
def generate_new_action(prompt, name):
    code = f'''from actions.actionsImport import * 

class {name}(Action):
    PROMPT_TEMPLATE: str = """
    {{instruction}}.
    {prompt}
    """

    name: str = "{name}"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp'''
    
    if name:
        # 建立 Python 檔案路徑
        file_path = os.path.join(os.getcwd(), "actions", f"{name}.py")
        print("File Path:", file_path)


        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)
    
    print(f"File created at: {file_path}")