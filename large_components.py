import components

class Checkpoint:
    def __init__(self,name:str):
        self.name = name
        self.frame_manager = components.frame_manager(self,self.name, shout=False)
        
    
