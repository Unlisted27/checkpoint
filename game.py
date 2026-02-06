import components, building_blocks
import arcade

#print(building_blocks.platoon.sections[0].groups[0].fireteams[0].members[0].name)
window = components.GameView(master_clock=building_blocks.clock)
window.setup()
arcade.run()