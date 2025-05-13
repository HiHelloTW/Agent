from actions._utils import * 

class NewsSummaryPrompt(Action):
    PROMPT_TEMPLATE: str = """
    {action_history}.
    Summarize the following news text, focusing on the events and their significance, without mentioning the subject of the news item.  The input text will be provided as a single string.
    """

    name: str = "NewsSummaryPrompt"

    async def run(self, instruction: str, step: int, action_history:list[str]):
        prompt = self.PROMPT_TEMPLATE.format(action_history=action_history)

        rsp = await self._aask(prompt)
        
        return rsp