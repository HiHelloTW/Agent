
from metagpt.schema import Message 
from metagpt.roles import Role 
from metagpt.logs import logger
import re
from metagpt.actions import UserRequirement
import os
import ast
import importlib.util

from actions._create_new_action import CreateNewAction
from metagpt.utils.repair_llm_raw_output import extract_state_value_from_output
from typing import TYPE_CHECKING, Iterable, Optional, Set, Type, Union
from metagpt.provider import HumanProvider

STATE_TEMPLATE = """You are a task agent named creater, and your goal is to complete a multi-step process.
You will be provided with conversation records and a specific step.
Your job is to determine the most appropriate stage to execute based solely on the specific task described in that individual step.
For this task, each step must be processed completely independently. The model is strictly prohibited from accessing, referencing, or inferring any information from previous, subsequent, or any other steps. Treat every step as a fully isolated input with no shared context or memory—do not carry over any knowledge or assumptions between steps under any circumstances. Failure to isolate steps will invalidate the evaluation.

===
Step:
{history}
===

Now is step: {step}

Please refer only to **Step {step}** to select the most appropriate stage.
You should choose a stage based on the literal stage described choose stage whitch completely right or choose 0 to creat new one.
Can you perform this step using this stage? If not, creat new one.
Please confirm whether the Kwak of step is consistent with the current stage
Just reply with a number, indicating the most suitable stage:

Available stages:
{states}


⚠️ Only respond with a number between 0 and {n_states}— no extra text, punctuation, or explanation.
"""

TO_IDEA_STEPS_TEMPLATE="""
Break down the following instruction into a list of independent steps. 
Each step must be self-contained and not rely on any previous step. 
Keep each step short and simple. 
Reduce the steps to the shortest possible steps. 
Only output the list of steps extracted strictly from the instruction without adding any extra steps. 
Finally, output only the steps with no extra text or explanations.
Use Kwak to add specific descriptions after each step, such as: Generate files, query data, generate pictures
Make sure every steps has a number and Translate into English.
eg: 1. creat a new csv.[Kwak: generate files]

Text:
"{idea}"
"""

def extract_tag_content(string):
    # 定義正則表達式，匹配 <XXX> 的模式
    match = re.search(r"<(.*?)>", string)
    if match:
        return match.group(1)  # 回傳匹配到的內容
    return None  # 如果沒有匹配到，回傳 None


def load_classes_from_folder(folder_path):
    """
    掃描資料夾中的所有 .py 檔案，動態匯入並回傳所有的 class（class 物件 list）
    """
    class_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and filename != "_utils.py" and filename != "_create_new_action.py":
            file_path = os.path.join(folder_path, filename)
            module_name = os.path.splitext(filename)[0]

            # 解析 AST 拿 class 名稱
            with open(file_path, "r", encoding="utf-8") as file:
                tree = ast.parse(file.read(), filename=filename)
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            # 動態載入模組
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                for cls_name in classes:
                    cls = getattr(module, cls_name, None)
                    if isinstance(cls, type):
                        class_list.append(cls)
            except Exception as e:
                print(f"⚠️ 載入 {filename} 時發生錯誤：{e}")

    return class_list

