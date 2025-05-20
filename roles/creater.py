from roles.utils import *
from metagpt.actions.action import Action
import inspect

class Creater(Role):
    name: str= ""
    idea: str= ""
    idea_by_steps: str= ""
    action_history: list[str]=[]
    actions: list[type] =[]
    action_step: int= 1
    actions = load_classes_from_folder('./actions')
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self._set_react_mode(react_mode="react", max_react_loop=3)
        self.set_actions([CreateNewAction, *self.actions])
    
    async def _react(self) -> Message:
        """Think first, then act, until the Role _think it is time to stop and requires no more todo.
        This is the standard think-act loop in the ReAct paper, which alternates thinking and acting in task solving, i.e. _think -> _act -> _think -> _act -> ...
        Use llm to select actions in _think dynamically
        """
        prompt = TO_IDEA_STEPS_TEMPLATE.format(idea = self.idea)
        self.idea_by_steps = await self.llm.aask(prompt)
        
        print(self.idea_by_steps)
        
        self.action_step = 1
        rsp = Message(content="No actions taken yet", cause_by=Action)  # will be overwritten after Role _act
        while self.action_step < self.rc.max_react_loop:
            # think
            print('----step:', self.action_step)
            await self._think()
            if self.rc.todo is None:
                break
            # act
            logger.debug(f"{self._setting}: {self.rc.state=}, will do {self.rc.todo}")
            rsp = await self._act()
            self.action_step += 1            
            print('self.actions', self.actions)
        return rsp  # return output from the last action
    
    async def _think(self) -> bool:
        """Consider what to do and decide on the next course of action. Return false if nothing can be done."""
        
        if self.recovered and self.rc.state >= 0:
            self._set_state(self.rc.state)  # action to run from recovered state
            self.recovered = False  # avoid max_react_loop out of work
            return True

        prompt = self._get_prefix()
        prompt += STATE_TEMPLATE.format(
            history=self.idea_by_steps,
            states="\n".join(self.states),
            n_states=len(self.states) - 1,
            previous_state=self.rc.state,
            step = self.action_step
        )
        
        print('----think prompt:', prompt)

        next_state = await self.llm.aask(prompt)
        print('next_state', next_state)
        next_state = extract_state_value_from_output(next_state)
        logger.debug(f"{prompt=}")

        if (not next_state.isdigit() and next_state != "-1") or int(next_state) not in range(-1, len(self.states)):
            logger.warning(f"Invalid answer of state, {next_state=}, will be set to -1")
            next_state = -1
        else:
            next_state = int(next_state)
            if next_state == -1:
                logger.info(f"End actions with {next_state=}")
        self._set_state(next_state)
        return True

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}")
        todo = self.rc.todo 
        
        rsp = await todo.run(
            instruction=self.idea_by_steps,
            step=self.action_step,
            action_history=self.action_history
            )
        
        if not isinstance(rsp, Action):
            self.action_history.append(rsp + "@@@")        
        if isinstance(rsp, Action):
            print('set actions')
            self.actions = load_classes_from_folder('./actions')
            self.set_actions([CreateNewAction, *self.actions])
            
            print('run created action')
            
            created_action_rsp = await rsp.run(
                instruction=self.idea_by_steps,
                step=self.action_step,
                action_history=self.action_history
                )
            self.action_history.append(created_action_rsp + "@@@")       
             
        print(self.action_history)
    
        