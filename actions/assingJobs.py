from actions.actionsImports import *

class AssignJobs(Action):
    PROMPT_TEMPLATE: str = """
    ## 
    "明智地分配工作，確保專案成功並鼓勵團隊合作。
    在每次任務分配時，你會明確說明每個成員的角色、任務的目標、完成的期限，以及可供使用的資源。
    如果有成員需要幫助或資源不足，你會提出建議或調整計劃。以下是團隊背景與需要完成的任務："
    
    示例：
    "團隊背景：    
    {roles}
        
    需要完成的任務：
    {context}
    
    請開始分配任務，並確保考慮到團隊背景成員的強項"
    決定後只用 "<成員名稱>" 生成以下文字 
    例如:
    <Leader>。
    """
    def __init__(self, name="AssignJobs", context=None, llm=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.context = context
        self.llm = llm
        
    async def run(self, context: str, roles: str):

        prompt = self.PROMPT_TEMPLATE.format(context=context, roles=roles)

        rsp = await self._aask(prompt)
        
        return rsp