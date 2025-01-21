from roles.rolesImport import *

class Leader(Role):
    name: str= ""
    profile: str = ""
    hire_roles: list[Role] = []
    
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}")
        todo = self.rc.todo 

        memories = self.get_memories()
        context ="\n".join(f"{msg.sent_from}: {msg.content}" for msg in memories)
        
        roles = "\n".join(f"{hire_role.name}: {hire_role.profile}" for hire_role in self.hire_roles)
        
        rsp = await todo.run(context=context, roles=roles)       
        
        sendTo = extract_tag_content(rsp)
        
        msg = Message(
            content=context,
            role=self.profile,
            cause_by=type(todo),
            sent_from=self.name,
            send_to=sendTo,
        )
        
        self.rc.memory.add(msg)

        return msg
