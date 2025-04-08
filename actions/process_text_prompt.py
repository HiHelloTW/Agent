from actions.utils import * 

class TextProcessorPrompt(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Process the following text, ignoring the subject line.  Generate a concise summary of the main points and key details.
    """

    name: str = "TextProcessorPrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp