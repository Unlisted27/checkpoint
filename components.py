from datetime import datetime
import random


class frame_manager:
    def __init__(self, owner, name:str="", shout:bool=False):
        self.owner = owner
        self.name = name
        self.shout = shout
        self.delta = 0
        self.last_frame_time = datetime.now()

    def on_frame(self):
        now = datetime.now()
        self.delta = (now - self.last_frame_time).total_seconds()
        self.last_frame_time = now

        if self.shout:
            print(f"[{self.name}] Frame advanced ({self.delta:.3f}s)")

        # call the owner's tick hook
        if hasattr(self.owner, "on_tick"):
            self.owner.on_tick(self.delta)

class Master_clock:
    def __init__(self):
        self.frame = 0
        self.observers = []   # anything that needs to react to time passing

    def register(self, obj:object):
        """Register an object that has a 'frame_manager'."""
        self.observers.append(obj)


    def advance(self):
        """Advance the frame and notify observers."""
        self.frame += 1
        print(f"--- Advancing to frame {self.frame} ---")
        for o in self.observers:
            o.frame_manager.on_frame()

class Weapon:
    def __init__(self, name:str, weight:int, damage:int, ammo_count:int, sustained_fire_rate:int=15, max_fire_rate:int=65):
        '''Fire rate is rounds per minute'''
        self.name = name
        self.weight = weight
        self.damage = damage
        self.ammo_count = ammo_count
        self.sustained_fire_rate = sustained_fire_rate
        self.max_fire_rate = max_fire_rate

class Stat:
    def __init__(self,base_value:int):
        self.base_value = base_value
        self.value = base_value
    def increase(self,amount:int):
        self.value += amount
    def decrease(self,amount:int):
        self.value -= amount

class Role:
    def __init__(self, name:str, weapon:Weapon):
        self.name = name
        self.weapon = weapon

class Soldier:
    def __init__(self, name:str, mobility:int, vision:int, mental_state:int, rank:str, role:Role="Rifleman"):
        self.name = name
        self.mobility = Stat(mobility)
        self.vision = Stat(vision)
        self.mental_state = Stat(mental_state)
        role = role
        self.rank = rank
        self.injuries = []
        self.frame_manager = frame_manager(
            owner=self,
            name=f"Soldier:{self.name}",
            shout=False
        )    
        def on_tick(self, delta: float):
            pass
            # this runs every frame
            # movement, morale decay, AI thinking, etc.

class Vehicle:
    def __init__(self, model:str):
        self.model = model
        self.frame_manager = frame_manager("Vehicle:"+self.model, shout=False)

class Fireteam:
    '''Fireteam is a small unit, typically consisting of 2 soldiers.'''
    def __init__(self, team_name:str, members:list[Soldier]):
        self.team_name = team_name
        self.members = members
        self.frame_manager = frame_manager("Fireteam:"+self.team_name, shout=True)

class Group:
    '''Group is a larger unit consisting of multiple fireteams (4 soldiers).'''
    def __init__(self, team_name:str, fireteams:list[Fireteam]):
        self.team_name = team_name
        self.fireteams = fireteams
        self.frame_manager = frame_manager("Group:"+self.team_name, shout=False)

class Section:
    '''Section is a unit consisting of two groups (8 soldiers).'''
    def __init__(self, squad_name:str, groups:list[Group]):
        self.squad_name = squad_name
        self.groups = groups
        self.frame_manager = frame_manager("Squad:"+self.squad_name, shout=True)

class PlatoonHQ:
    '''PlatoonHQ is the command unit of a platoon.'''
    def __init__(self, members:list[Soldier]):
        self.members = members
        self.frame_manager = frame_manager("PlatoonHQ", shout=False)

class Platoon:
    '''Platoon is a unit consisting of 3 sections, plus platoon HQ (~30 soldiers).'''
    def __init__(self, platoon_name:str, sections:list[Section]):
        self.platoon_name = platoon_name
        self.sections = sections
        self.frame_manager = frame_manager("Platoon:"+self.platoon_name, shout=True)


