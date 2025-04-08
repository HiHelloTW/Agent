from actions.utils import * 

class KeyInfoExtractor(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Extract key information from the following text, focusing on entities, dates, locations, and events.  Identify relationships between these elements.  Present the findings in a structured format suitable for knowledge graph construction.  The text may contain irrelevant or distracting information; prioritize the core factual details.
    """

    name: str = "KeyInfoExtractor"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp