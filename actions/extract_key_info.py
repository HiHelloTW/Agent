from actions.utils import * 

class KeyInfoExtractor(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Extract key information from the following text, focusing on entities, dates, locations, and events.  Identify the relationships between these elements.  Represent the extracted information in a structured format suitable for knowledge graph construction or database population.  The text should be processed to remove any subjective opinions or biases present.  Prioritize factual information.
    """

    name: str = "KeyInfoExtractor"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp