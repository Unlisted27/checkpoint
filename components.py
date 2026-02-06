from datetime import datetime
import random, arcade

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Checkpoint"

draw_buffer = [] #Every sprite that will be drawn this frame

# components.py (partial)
from datetime import datetime
import random, arcade

# keep your draw_buffer here (module-level is fine for now)
draw_buffer = []

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Checkpoint"

class GameView(arcade.Window):
    def __init__(self, master_clock=None):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # The Master_clock instance that we will advance each on_update
        # Pass it in from game.py to avoid circular imports.
        self.master_clock = master_clock

        # record start time for FPS/stats
        self._start_time = datetime.now()
        self._stopped_at_frame = None

    def setup(self):
        pass

    def on_update(self, delta_time: float):
        # Advance the Master_clock if provided
        if self.master_clock is not None:
            self.master_clock.advance()

            # Example: stop after 1000 frames
            if self.master_clock.frame == 1000:
                # compute stats and print (you can also set a flag)
                total_seconds = (datetime.now() - self._start_time).total_seconds()
                print("Simulation paused at frame 1000")
                print("Total simulation time:", total_seconds, "seconds")
                print("Average FPS:", self.master_clock.frame / max(total_seconds, 1e-6))
                self._stopped_at_frame = self.master_clock.frame

                # Close the arcade window -> arcade.run() will return
                arcade.close_window()

    def on_draw(self):
        self.clear()
        # Draw sprites stored in module-level draw_buffer
        for sprite in draw_buffer:
            # draw using Sprite.draw()
            if sprite is not None:
                arcade.draw_sprite(sprite)
        # Clear buffer after drawing
        draw_buffer.clear()


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
    global draw_buffer
    def __init__(self, name:str, rank:str, role:Role, sprite = None):
        super().__init__()
        self.name = name
        self.role = role
        self.rank = rank
        self.sprite = None  # Placeholder for graphical representation
        self.frame_manager = frame_manager(
            owner=self,
            name=f"Soldier:{self.name}",
            shout=False
        )    
        # Variable to hold our texture for our player
        self.texture = arcade.load_texture(
            "textures/soldier_textures/soldier.jpg"
        )

        # Separate variable that holds the player sprite
        if self.texture is not None:
            self.sprite = arcade.Sprite(self.texture)
            print(f"{self.name} - Texture loaded successfully!")
        else:
            print(f"{self.name} - Error loading texture!")
        self.sprite.center_x = 64
        self.sprite.center_y = 128
    def on_tick(self, delta: float):     
        #draw_buffer.append(self.sprite)  # Add soldier sprite to draw buffer each frame
        if self.role.name == "Platoon Leader":
            self.sprite.center_x += 100*delta  # Move right each frame
            draw_buffer.append(self.sprite)  # Add soldier sprite to draw buffer each frame
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
