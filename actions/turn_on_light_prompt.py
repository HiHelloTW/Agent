from actions.utils import * 

class TurnOnLightPrompt(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Locate the light switch. Assess the switch's state. If the switch is off, move it to the on position. Verify the light is illuminated.
    """

    name: str = "TurnOnLightPrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp