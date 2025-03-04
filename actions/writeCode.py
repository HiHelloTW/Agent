from actions.actionsImport import *

class WriteCodes(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Return ``` your_code_here ``` with NO other texts,
    your code:
    """

    name: str = "SimpleWriteCode"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)

        code_text = WriteCodes.parse_code(rsp)
        
        return code_text

    @staticmethod
    def parse_code(rsp):
        pattern = r"```*```"
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text