from actions._utils import * 

class GenerateNewsText(Action):
    PROMPT_TEMPLATE: str = """ 
    If Action history contains content, follow the Action history in the <<>> and Generate a news article text.; otherwise, just Generate a news article text..

    <<Action history:
    {action_history}.
    >>
    """

    name: str = "GenerateNewsText"

    async def run(self, instruction: str, step: int, action_history:list[str]):
        prompt = self.PROMPT_TEMPLATE.format(action_history=action_history)

        rsp = await self._aask(prompt)
        
        return rsp