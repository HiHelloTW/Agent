
from metagpt.schema import Message 
from metagpt.roles import Role 
from metagpt.logs import logger
import re
from metagpt.actions import UserRequirement

from actions.write_code import WriteCodes
from actions.assing_jobs import AssingJobs
from actions.create_new_action import CreateNewAction

def extract_tag_content(string):
    # 定義正則表達式，匹配 <XXX> 的模式
    match = re.search(r"<(.*?)>", string)
    if match:
        return match.group(1)  # 回傳匹配到的內容
    return None  # 如果沒有匹配到，回傳 None