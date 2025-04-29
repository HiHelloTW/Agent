from actions.utils import * 

class PutSweetPotatoAside(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Put the sweet potato aside.
    """

    name: str = "PutSweetPotatoAside"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp