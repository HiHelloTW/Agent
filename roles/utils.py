
from metagpt.schema import Message 
from metagpt.roles import Role 
from metagpt.logs import logger
import re
from metagpt.actions import UserRequirement
import os
import ast
import importlib.util

from actions.write_code import WriteCodes
from actions.assing_jobs import AssingJobs
from actions.create_new_action import CreateNewAction

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
        if filename.endswith(".py") and filename != "utils.py":
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