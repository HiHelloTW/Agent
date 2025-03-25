from actions.utils import * 

class EnglishToFrenchTranslator(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Translate the English sentence 'The quick brown fox jumps over the lazy dog' into French.
    """

    name: str = "EnglishToFrenchTranslator"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp