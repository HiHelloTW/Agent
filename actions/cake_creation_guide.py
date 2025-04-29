from actions.utils import * 

class CakeCreationGuide(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Provide a step-by-step guide on how to create a cake, including ingredient lists for different types of cakes (e.g., chocolate, vanilla, sponge), baking instructions, frosting techniques, and decorating ideas.  The guide should be comprehensive enough for a beginner baker.
    """

    name: str = "CakeCreationGuide"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp