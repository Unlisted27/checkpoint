import components, random

clock = components.Master_clock()

# The platoon
# Structure:
# Platoon -> Squads -> Teams -> Soldiers
# Bravo platoon 2
# ---> Squad 1

class Weapons:
    C7A2 = components.Weapon("C7A2", 4.58, 100, 30, 15, 65, "Standard issue assault rifle for infantry.")
    C9A2 = components.Weapon("C9A2", 11.35, 100, 200, 50, 100, "Standard issue light machine gun.")

class Roles:
    Rifleman = components.Role("Rifleman",Weapons.C7A2)
    Section_commander = components.Role("Section Commander",Weapons.C7A2)
    Section_2IC = components.Role("Section 2IC",Weapons.C7A2)
    Anti_tank_Specialist = components.Role("Anti-tank Specialist",Weapons.C7A2)
    Medic = components.Role("Medic",Weapons.C7A2)
    Heavy_machine_gunner = components.Role("Heavy Machine Gunner",Weapons.C9A2)
    Light_machine_Gunner = components.Role("Light Machine Gunner",Weapons.C9A2)
    

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

def gen_soldiers(clock:components.Master_clock,count:int):
    soldiers = []
    for _ in range(count):
        import random
        name = genname()
        mobility = random.randint(1,10)
        vision = random.randint(1,10)
        mental_state = random.randint(1,10)
        soldier = components.Soldier(name, mobility, vision, mental_state, "Private", Roles.Rifleman)
        clock.register(soldier)
        soldiers.append(soldier)
    return soldiers

def gen_platoon(clock:components.Master_clock,platoon_name:str="1"):
    sections = []
    for sectioni in range(3):
        groups = []
        team_names = ["Alpha", "Bravo", "Charlie", "Delta"]
        for groupi in range(2):
            teams = []
            for teami in range(2):
                team = components.Fireteam(f"Fireteam {platoon_name}{sectioni+1}{team_names[teami+groupi*2]}", gen_soldiers(clock,2))
                clock.register(team)
                teams.append(team)
            group = components.Group(f"Group {platoon_name}{sectioni+1}{groupi+1}", teams)
            clock.register(group)
            groups.append(group)
        section = components.Section(f"Section {platoon_name}{sectioni+1}", groups)
        clock.register(section)
        sections.append(section)
    platoon_hq_members = gen_soldiers(clock,6)
    platoon_hq = components.PlatoonHQ(platoon_hq_members)
    clock.register(platoon_hq)
    platoon = components.Platoon(f"Platoon {platoon_name}", sections, platoon_hq)
    clock.register(platoon)
    return platoon


platoon = gen_platoon(clock)

#for soldier in alpha_team.members:
    #print(f"Soldier {soldier.name}: Mobility={soldier.mobility.value}, Vision={soldier.vision.value}, Mental State={soldier.mental_state.value}")