from actions._utils import * 

class TodaysNewsQuery(Action):
    PROMPT_TEMPLATE: str = """ 
    If Action history contains content, follow the Action history in the <<>> and Query today's news.; otherwise, just Query today's news..

    <<Action history:
    {action_history}.
    >>
    """

    name: str = "TodaysNewsQuery"

    async def run(self, instruction: str, step: int, action_history:list[str]):
        prompt = self.PROMPT_TEMPLATE.format(action_history=action_history)

        rsp = await self._aask(prompt)
        
        return rsp