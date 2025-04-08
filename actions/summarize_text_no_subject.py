from actions.utils import * 

class TextSummarizerNoSubject(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Summarize the key information and insights presented in the following text, focusing on the main points and excluding any subject-related details.  Provide a concise overview of the content.
    """

    name: str = "TextSummarizerNoSubject"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp