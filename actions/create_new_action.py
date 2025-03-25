import json
from actions.utils import *
class CreateNewAction(Action):
    PROMPT_TEMPLATE: str = """
    Please read the following in """""" carefully, and step by step handle the following tasks
    """"{instruction} """"
    
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
        generate_new_action(*extract_prompt_name(rsp))
        
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
        print("File Path:", file_path)


        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)
    
    print(f"File created at: {file_path}")