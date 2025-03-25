from actions.utils import * 

class CatTrainingPrompt(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Train a cat using positive reinforcement techniques. This includes establishing a consistent daily routine, using treats and praise to reward desired behaviors, employing clicker training if desired, teaching basic commands like 'sit', 'stay', and 'come', providing environmental enrichment, redirecting unwanted behaviors, and observing the cat's body language.  Remember patience and consistency are key.  Seek professional help if needed.
    """

    name: str = "CatTrainingPrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp