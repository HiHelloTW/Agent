from actions.actionsImport import * 

class HelloWorldJS(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Write a program in JavaScript that displays the text 'Hello, world!' on the console.
    """

    name: str = "HelloWorldJS"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp