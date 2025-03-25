from actions.utils import * 

class FoldPaperAirplane(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    摺紙飛機
    """

    name: str = "FoldPaperAirplane"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp