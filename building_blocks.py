import components, random

clock = components.Master_clock()

# The platoon
# Structure:
# Platoon -> Sections -> Teams -> Soldiers
# Bravo platoon 2
# ---> Platoon HQ
# -------> Platoon Commander
# -------> Platoon 2IC
# -------> Signaller
# -------> Medic
# ---> Section 1
# -------> Group 1
# ----------> Fireteams 11A and 11B
# -------> Group 2
# ----------> Fireteams 12C and 12D
# ---> Section 2
# -------> Group 1
# ----------> Fireteams 21A and 21B
# -------> Group 2
# ----------> Fireteams 22C and 22D
# ---> Section 3
# -------> Group 1
# ----------> Fireteams 31A and 31B
# -------> Group 2
# ----------> Fireteams 32C and 32D

# Damage stats still need to be modified, I will likely rework the entire weapons system when I implement combat mechanics.
class soldier_weapons:
    # Stats for these weapons were found on the Canadian government's official website
    C7A2 = components.Weapon("C7A2", 4.58, 100, 30, 15, 65, "Standard issue assault rifle for infantry.") #Stats from https://www.canada.ca/en/army/services/equipment/weapons/c7a2-automatic-rifle.html
    C9A2 = components.Weapon("C9A2", 11.35, 100, 200, 50, 100, "Standard issue light machine gun.") #Stats from https://www.canada.ca/en/army/services/equipment/weapons/c9a2-light-machine-gun.html

class militant_weapons:
    # Stats for these weapons were ai generated, cannot attest to their accuracy at this time, will update if I remember to.
    AK47 = components.Weapon("AK-47", 3.47, 100, 30, 10, 60, "Common assault rifle used by militant groups.")
    RPK = components.Weapon("RPK", 7.0, 100, 75, 40, 90, "Light machine gun variant of the AK-47 used by militant groups.")

class soldier_roles:
    Rifleman = components.Role("Rifleman",soldier_weapons.C7A2)
    Section_commander = components.Role("Section Commander",soldier_weapons.C7A2)
    Section_2IC = components.Role("Section 2IC",soldier_weapons.C7A2)
    Anti_tank_Specialist = components.Role("Anti-tank Specialist",soldier_weapons.C7A2)
    Medic = components.Role("Medic",soldier_weapons.C7A2)
    Heavy_machine_gunner = components.Role("Heavy Machine Gunner",soldier_weapons.C9A2)
    Light_machine_Gunner = components.Role("Light Machine Gunner",soldier_weapons.C9A2)
    
class militant_roles:
    Fighter = components.Role("Fighter",militant_weapons.AK47)
    Anti_tank_Specialist = components.Role("Anti-tank Specialist",militant_weapons.AK47)
    Heavy_machine_gunner = components.Role("Heavy Machine Gunner",militant_weapons.RPK)
# Generators

class name_parts:
    start_sounds = [
    "Al", "An", "Br", "Ca", "Ch", "Da", "El", "Ja", "Jo", "Ka",
    "La", "Ma", "Mi", "Na", "Ni", "Pa", "Ra", "Sa", "Sh", "Ta",
    "Te", "Tr", "Va", "Wi", "Za", "Ben", "Cam", "Dan", "Eli", "Jon",
    "Kal", "Leo", "Mar", "Max", "Nat", "Noa", "Sam", "Ste", "Tor", "Vic",
    "Wes", "Zan", "Ash", "Cole", "Dre", "Jax", "Kris", "Luke", "Ryan"
    ]

    middle_sounds = [
        "a", "e", "i", "o", "u", "ae", "ai", "ea", "ee", "io",
        "ar", "er", "ir", "or", "ur", "an", "en", "in", "on", "un",
        "el", "al", "il", "ol", "ul", "ra", "re", "ri", "ro", "ru",
        "ma", "na", "la", "ta", "da", "cha", "sha", "lo", "mi", "ni",
        "so", "ti", "vi", "ya", "za", "ke", "mo", "pa", "sa", "to"
    ]

    end_sounds = [
        "n", "r", "s", "l", "k", "m", "t", "d", "y", "e",
        "er", "on", "en", "an", "in", "ton", "son", "ley", "lin", "man",
        "ric", "den", "vin", "ford", "well", "hart", "son", "sky", "wood", "more",
        "ian", "ette", "lyn", "ette", "ette", "ria", "na", "la", "ah", "ie",
        "o", "us", "ix", "or", "is", "el", "ar", "eth", "io", "as"
    ]

def genname():
    length = random.randint(2,3)
    if length == 2:
        name = name_parts.start_sounds[random.randint(0,len(name_parts.start_sounds)-1)] + name_parts.end_sounds[random.randint(0,len(name_parts.end_sounds)-1)]
    if length == 3:
        name = name_parts.start_sounds[random.randint(0,len(name_parts.start_sounds)-1)] + name_parts.middle_sounds[random.randint(0,len(name_parts.middle_sounds)-1)] + name_parts.end_sounds[random.randint(0,len(name_parts.end_sounds)-1)]
    return(name)

# Friendly force generators
def gen_soldiers(clock:components.Master_clock,count:int,rank="Private",role=soldier_roles.Rifleman):
    soldiers = []
    for _ in range(count):
        import random
        name = genname()
        mobility = random.randint(1,10)
        vision = random.randint(1,10)
        mental_state = random.randint(1,10)
        soldier = components.Soldier(name, mobility, vision, mental_state, rank, role)
        clock.register(soldier)
        soldiers.append(soldier)
    return soldiers

def ft(name, soldiers):
    return components.Fireteam(name, soldiers)

def grp(name, fireteams):
    return components.Group(name, fireteams)

def create_section(clock: components.Master_clock, section_name: str):

    # GROUP 1
    ft_A = ft(f"{section_name}1A", [
        gen_soldiers(clock, 1, "Sergeant", soldier_roles.Section_commander)[0],  # FT leader / Sect Comd
        gen_soldiers(clock, 1)[0],                                       # Rifleman
        gen_soldiers(clock, 1)[0],                                       # Grenadier
    ])

    ft_B = ft(f"{section_name}1B", [
        gen_soldiers(clock, 1, "Corporal")[0],                           # FT leader
        gen_soldiers(clock, 1, role=soldier_roles.Light_machine_Gunner)[0],
    ])

    group_1 = grp("Group 1", [ft_A, ft_B])

    # GROUP 2
    ft_C = ft(f"{section_name}2C", [
        gen_soldiers(clock, 1, "Corporal", soldier_roles.Section_2IC)[0],        # FT leader / 2IC
        gen_soldiers(clock, 1, role=soldier_roles.Light_machine_Gunner)[0],
    ])

    ft_D = ft(f"{section_name}2D", [
        gen_soldiers(clock, 1, "Corporal")[0],                           # FT leader / 3IC
        gen_soldiers(clock, 1)[0],
        gen_soldiers(clock, 1)[0],
    ])

    group_2 = grp("Group 2", [ft_C, ft_D])

    section = components.Section(section_name, [group_1, group_2])

    # register unit clocks
    clock.register(section)
    clock.register(group_1)
    clock.register(group_2)
    for ftm in [ft_A, ft_B, ft_C, ft_D]:
        clock.register(ftm)

    return section

def create_platoon_hq(clock: components.Master_clock):
    members = [
        gen_soldiers(clock, 1, "Lieutenant")[0],     # Platoon Commander
        gen_soldiers(clock, 1, "Sergeant")[0],       # Platoon 2IC
        gen_soldiers(clock, 1, "Corporal")[0],       # Signaller
        gen_soldiers(clock, 1, "Corporal", soldier_roles.Medic)[0],
    ]

    hq = components.PlatoonHQ(members)
    clock.register(hq)
    return hq

def create_platoon(clock: components.Master_clock, name="Bravo Platoon 2"):
    sections = [
        create_section(clock, "1"),
        create_section(clock, "2"),
        create_section(clock, "3"),
    ]

    platoon_hq = create_platoon_hq(clock)

    platoon = components.Platoon(name, sections, platoon_hq)
    clock.register(platoon)

    return platoon

#Faction forces generation
def gen_faction(clock:components.Master_clock, name:str=None,friendly:bool=False):
    if name is None:
        name = genname() + " faction"
    compliance = random.randint(0,5) if friendly else random.randint(-5,0)  # Factions are generally hostile to occupation forces
    faction = components.Faction(name,compliance)
    clock.register(faction)
    return faction

def gen_militants(clock:components.Master_clock,count:int,role:components.Role,region:components.Region):
    militants = []
    for _ in range(count):
        name = genname()
        mobility = random.randint(1,10)
        vision = random.randint(1,10)
        mental_state = random.randint(1,10)
        attitude = random.randint(-3,2) # Remember, the lower the attitude, the more hostile they are
        attitude += region.stability / 4  # More stable regions produce less hostile militants
        militant = components.Human(name,role,region,mobility,vision,mental_state,attitude)
        clock.register(militant)
        militants.append(militant)
    return militants

# Object creation
# Friendly forces
platoon = create_platoon(clock)

region1 = components.Region(genname(), compliance=1,stability=0) #Was considering making a new name generator for regions, but the DEI team said I best not...

# Faction forces
class factions:
    resistance = gen_faction(clock, "Resistance", friendly=True)
    insurgents = gen_faction(clock, "Insurgents", friendly=False)
    resistance.add_members(gen_militants(clock, 20, militant_roles.Fighter, region1))
    insurgents.add_members(gen_militants(clock, 20, militant_roles.Fighter, region1))