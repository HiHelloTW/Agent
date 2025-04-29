from roles.utils import *
from metagpt.actions.action import Action
import inspect

class Creater(Role):
    name: str= ""
    idea: str= ""
    actions: list[type]    
    actions = load_classes_from_folder('./actions')
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        
        self.set_actions([CreateNewAction, *self.actions])
    
        
    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}")
        todo = self.rc.todo 
        print('todo: ', todo)
        rsp = await todo.run(instruction=self.idea)
        
        if isinstance(rsp, Action):
            print('run created action')
            created_action_rsp = await rsp.run(instruction=self.idea)
            print(created_action_rsp)
