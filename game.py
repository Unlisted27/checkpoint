import components, building_blocks


#print(building_blocks.platoon.sections[0].groups[0].fireteams[0].members[0].name)
start_time = components.datetime.now()
while True:
    building_blocks.clock.advance()
    if building_blocks.clock.frame == 1000:
        #pause logic
        print("Simulation paused at frame 5000--------------------------------")
        print("Total simulation time:", (components.datetime.now() - start_time).total_seconds(), "seconds")
        print("That's an average frame rate of", building_blocks.clock.frame / (components.datetime.now() - start_time).total_seconds(), "frames per second")
        print(f"The platoon commander is: {building_blocks.platoon.platoon_hq.members[0].rank} {building_blocks.platoon.platoon_hq.members[0].name}")
        input("Press Enter to continue...")