from roles.utils import *
import subprocess
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
        print('todo:', todo)
        print('todo.run:', todo.run)
                
        rsp = await todo.run(instruction=self.idea)    
        
        print(1,todo.name)
        if todo.name == 'CreateNewAction':
            print('run py')
            subprocess.run(["python", "./run.py"]) 
        
        return rsp
