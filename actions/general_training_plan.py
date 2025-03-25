from actions.utils import * 

class GeneralTrainingPlan(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    Develop a training plan that includes defining specific, measurable, achievable, relevant, and time-bound (SMART) goals; utilizing positive reinforcement methods such as treats, praise, or toys; maintaining consistency in commands and rewards; conducting short, frequent training sessions; exercising patience and adaptability; providing positive feedback; and concluding each session with a successful behavior.
    """

    name: str = "GeneralTrainingPlan"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp