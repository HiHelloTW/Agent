from actions.utils import * 

class BuyDrinkPrompt(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    You need to buy a bottle of drink.  Specify the type of drink you want to buy, the location where you will buy it (e.g., a specific store or vending machine), and how you will pay for it (e.g., cash, credit card, mobile payment).
    """

    name: str = "BuyDrinkPrompt"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp