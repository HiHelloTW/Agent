from actions.utils import * 

class PlantTreePrompt(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    plant the tree
    """

    name: str = "PlantTreePrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp