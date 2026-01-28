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
        #print(f"--- Advancing to frame {self.frame} ---")
        for o in self.observers:
            o.frame_manager.on_frame()

class Weapon:
    def __init__(self, name:str, weight:int, damage:int, ammo_count:int, sustained_fire_rate:int, max_fire_rate:int, description:str=""):
        '''Fire rate is rounds per minute'''
        self.name = name
        self.weight = weight
        self.damage = damage
        self.ammo_count = ammo_count
        self.sustained_fire_rate = sustained_fire_rate
        self.max_fire_rate = max_fire_rate
        self.description = description

#Whats the point of a class that acts like an int? Its for storing a stat's base value and current value separately.
class Stat:
    def __init__(self,base_value:int):
        self.base_value = base_value
        self.value = base_value
    def increase(self,amount:int):
        self.value += amount
    def decrease(self,amount:int):
        self.value -= amount

class Body:
    def __init__(self, mobility:int=random.randint(1,10), vision:int=random.randint(1,10), mental_state:int=random.randint(1,10)):
        self.health = Stat(100)
        self.blood_amount = Stat(100)  # percentage
        self.mobility = Stat(mobility)
        self.vision = Stat(vision)
        self.mental_state = Stat(mental_state)
        self.injuries = []

class Role:
    def __init__(self, name:str, weapon:Weapon):
        self.name = name
        self.weapon = weapon

class Soldier(Body):
    def __init__(self, name:str, rank:str, role:Role="Rifleman"):
        super().__init__()
        self.name = name
        role = role
        self.rank = rank
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
        self.frame_manager = frame_manager(self,self.model, shout=False)

class Fireteam:
    '''Fireteam is a small unit, typically consisting of 2 soldiers.'''
    def __init__(self, team_name:str, members:list[Soldier]):
        self.team_name = team_name
        self.members = members
        self.frame_manager = frame_manager(self,self.team_name, shout=False)

class Group:
    '''Group is a larger unit consisting of multiple fireteams (4 soldiers).'''
    def __init__(self, team_name:str, fireteams:list[Fireteam]):
        self.team_name = team_name
        self.fireteams = fireteams
        self.frame_manager = frame_manager(self,self.team_name, shout=False)

class Section:
    '''Section is a unit consisting of two groups (8 soldiers).'''
    def __init__(self, squad_name:str, groups:list[Group]):
        self.squad_name = squad_name
        self.groups = groups
        self.frame_manager = frame_manager(self,self.squad_name, shout=False)

class PlatoonHQ:
    '''PlatoonHQ is the command unit of a platoon.'''
    def __init__(self, members:list[Soldier]):
        self.members = members
        self.frame_manager = frame_manager(self,"PlatoonHQ", shout=False)

class Platoon:
    '''Platoon is a unit consisting of 3 sections, plus platoon HQ (~30 soldiers).'''
    def __init__(self, platoon_name:str, sections:list[Section], platoon_hq:PlatoonHQ):
        self.platoon_name = platoon_name
        self.sections = sections
        self.platoon_hq = platoon_hq
        self.frame_manager = frame_manager(self,self.platoon_name, shout=False)

class Region:
    def __init__(self, name:str, compliance:int=0, stability:int=0):
        self.name = name
        self.stability = stability  # Overall region stability, this affects how factions will later change their attitudes
        self.compliance = compliance  # Overall region compliance, affects civillian compliance. Effectively the people's attitude towards the occupying force.
        
class Faction:
    def __init__(self, name:str, compliance:int=0):
        self.name = name
        self.compliance:int = compliance  # Overall faction compliance, affects member attitude
        self.members:list = []
        self.manpower:int = 0
        self.frame_manager = frame_manager(self,"a faction force", shout=False)
    
    def add_members(self, new_members:list['Human']):
        for member in new_members:
            self.members.append(member)
            member.on_join_faction(self)
        self.manpower = len(self.members)

class Human(Body):
    def __init__(self, name:str, role:Role, region:Region, attitude:int = 0):
        super().__init__()
        self.name = name
        self.role = role
        self.region = region
        self.faction = None
        #The lower the attitude, the more hostile. This will determine their compliance with the checkpoint. Anti occupation factions will give a large debuff to their members' attitude which will make them more hostile.
        self.attitude = attitude + region.compliance
        self.injuries = []
        self.frame_manager = frame_manager(self,self.name, shout=False)
    def on_join_faction(self, faction:Faction):
        self.faction = faction
        # Recalculate attitude based on faction compliance. If the faction is friendly, then the region attitude bonus (or debuff) also applies, but if the faction is hostile, the region compliance does not influence the person's attitude.
        self.attitude = self.faction.compliance + self.attitude + self.region.compliance if self.faction.compliance > 0 else self.faction.compliance + self.attitude

# Checkpoint components
class Obstacle:
    def __init__(self, barrier_type:str, vehicle_stopping_power:int, human_stopping_power:int, climeable:bool, cover_value:int):
        self.barrier_type = barrier_type # Just the name (ex: Concertina Wire)
        self.vehicle_stopping_power = vehicle_stopping_power # How effective it is against vehicles, a value between 1 and 100. When a vehicle impacts, a random roll will be made to determine how damaged the vehicle and its occupants becomes.
        self.human_stopping_power = human_stopping_power # How effective it is against humans, a value between 1 and 100. When a human attempts to breach, a random roll will be made to determine how injured they become.
        self.climeable = climeable # Can humans climb over it? If this value is true, the stopping power now represents the time it takes to climb, but they will not be damaged.
        self.cover_value = cover_value # How much cover it provides to humans behind it, a value between 0 and 100. While in a cover state, this value reduces the chance of getting hit, and incoming damage.
        self.frame_manager = frame_manager(self,self.barrier_type, shout=False)

class Serpentine():
    def __init__(self):
        self.obstacles = []
        self.frame_manager = frame_manager(self,"Serpentine", shout=False)
    def add_obstacles(self, obstacles:list[Obstacle]):
        for obstacle in obstacles:
            self.obstacles.append(obstacle)
    def debug_show_obstacles(self):
        for obstacle in self.obstacles:
            print(f"Obstacle: {obstacle.barrier_type}")

class Guardian_angels:
    def __init__(self):
        pass

class Troop_positions():
    def __init__(self):
        pass