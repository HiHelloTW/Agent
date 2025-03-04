from roles.rolesImport import *

class Leader(Role):
    name: str= ""
    idea: str= ""
    profile: str = ""
    hire_roles: list[Role] = []
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self.set_actions([CreateNewAction])
    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}")
        todo = self.rc.todo 
                
        rsp = await todo.run(instruction=self.idea)       

        return rsp
