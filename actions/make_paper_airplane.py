from actions.utils import * 

class PaperAirplaneInstructions(Action):
    PROMPT_TEMPLATE: str = """
    {instruction}.
    1. Start with a rectangular piece of paper. Lay it flat with the longer side horizontal.
2. Fold in half lengthwise; crease sharply, and unfold. 
3. Fold the top two corners to the center crease, aligning edges neatly.
4. Fold the top edges (now triangular flaps) down again, aligning the top edges with the center crease.
5. Fold the entire model in half along the center crease, bringing the two folded sides together. Crease sharply.
6. Fold down the wings along a crease roughly parallel to the body; adjust the angle for desired flight characteristics (steeper for stability, shallower for speed).
7. (Optional) Adjust wing flaps by folding small sections up or down at the tips.
8. Hold the airplane by the body, just behind the wings. Throw it gently with a smooth, overhand motion.
    """

    name: str = "PaperAirplaneInstructions"

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)

        rsp = await self._aask(prompt)
        
        return rsp