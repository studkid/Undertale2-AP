from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region
from .Locations import UT2Location, location_table, event_location_table
from Options import Choice
from .Options import UT2Options, AquariumSanity, ShuffleFishingMissions, RelaxRankNeedsPass, EndingGoal, CardSanity, EarlyBeach, LevelSanity

class UT2RegionData(NamedTuple):
    locations: Optional[List[str]]
    exits: Optional[List[str]]

def create_regions(multiworld: MultiWorld, player: int, options: UT2Options):
    regions: Dict[str, UT2RegionData] = {
        "Menu":                     UT2RegionData(None, ["Landing", "Special Enemies", "Early Levelsanity"]),
        "Special Enemies":          UT2RegionData([], []),
        "Early Levelsanity":        UT2RegionData([], ["Mid Levelsanity"]),
        "Mid Levelsanity":          UT2RegionData([], ["Late Levelsanity"]),
        "Late Levelsanity":         UT2RegionData([], []),

        "Landing":                  UT2RegionData([], ["Ruins Main", "Warehouse"]),
        "Ruins Main":               UT2RegionData([], ["Ruins Sewers", "Scopestablook", "Rest Zone"]),
        "Ruins Sewers":             UT2RegionData([], ["Ruins Lake"]),
        "Rest Zone":                UT2RegionData([], []),
        "Scopestablook":            UT2RegionData([], ["Ruins Lake"]),
        "Ruins Lake":               UT2RegionData([], ["Ruins Tree"]),
        "Ruins Tree":               UT2RegionData([], ["Archives Pit", "Swamp"]),
        
        "Archives Pit":             UT2RegionData([], ["Archives Sewers", "Archives Back", "Frogue Chamber"]),
        "Archives Sewers":          UT2RegionData([], []),
        "Archives Back":            UT2RegionData([], ["Hotden"]),
        "Hotden":                   UT2RegionData([], ["Prison Cells"]),
        "Frogue Chamber":           UT2RegionData([], []),

        "Swamp":                    UT2RegionData([], ["Spark Chamber"]),
        "Spark Chamber":            UT2RegionData([], []),

        "Prison Cells":             UT2RegionData([], ["Prison Puzzle", "Prison Kitchen"]),
        "Prison Puzzle":            UT2RegionData([], []),
        "Prison Kitchen":           UT2RegionData([], ["Prison Office"]),
        "Prison Office":            UT2RegionData([], ["Beach Entry"]),

        "Beach Entry":              UT2RegionData([], ["Beach Relax 1", "Greenhorn Shore", "Beach Post Boss", "Miku Zone"]),
        "Beach Relax 1":            UT2RegionData([], ["Beach Relax 2"]),
        "Beach Relax 2":            UT2RegionData([], ["Beach Relax 3"]),
        "Beach Relax 3":            UT2RegionData([], ["Beach Relax 4"]),
        "Beach Relax 4":            UT2RegionData([], ["Beach Relax 5"]),
        "Beach Relax 5":            UT2RegionData([], ["Beach Relax 6"]),
        "Beach Relax 6":            UT2RegionData([], ["Beach Relax 7"]),
        "Beach Relax 7":            UT2RegionData([], ["Beach Relax 8"]),
        "Beach Relax 8":            UT2RegionData([], []),
        "Greenhorn Shore":          UT2RegionData([], ["Breadcrumb Bay", "Rust Gear Gulf", "Aquarium", "Big Bone Bay", "Chemical Waste Zone", "Stardrop Tree"]),
        "Breadcrumb Bay":           UT2RegionData([], ["Melonbread Cove"]),
        "Melonbread Cove":          UT2RegionData([], ["Pudding"]),
        "Pudding":                  UT2RegionData([], []),
        "Aquarium":                 UT2RegionData([], []),
        "Rust Gear Gulf":           UT2RegionData([], []),
        "Chemical Waste Zone":      UT2RegionData([], []),
        "Big Bone Bay":             UT2RegionData([], []),
        "Stardrop Tree":            UT2RegionData([], []),
        "Beach Post Boss":          UT2RegionData([], ["Toriel House", "Exit"]),
        "Miku Zone":                UT2RegionData([], []),
        
        "Toriel House":             UT2RegionData([], ["Toriel Roof", "Mario Zone", "Toriel Basement", ]),
        "Toriel Roof":              UT2RegionData([], ["Server"]),
        "Toriel Basement":          UT2RegionData([], []),
        "Mario Zone":               UT2RegionData([], []),
        "Exit":                     UT2RegionData([], ["Exit Back", "Flowey Room"]),
        "Exit Back":                UT2RegionData([], []),
        "Flowey Room":              UT2RegionData([], []),
        
        "Server":                   UT2RegionData([], ["Server Settings"]),
        "Server Settings":          UT2RegionData([], []),

        "Warehouse":                UT2RegionData([], ["Marisa Hall"]),
        "Marisa Hall":              UT2RegionData([], ["Heaven"]),
        "Heaven":                   UT2RegionData([], ["Post Game"]),
        "Post Game":                UT2RegionData([], []),
    }

    if options.early_beach != EarlyBeach.option_false:
        regions["Rest Zone"].exits.append("Beach Entry")

    for name, data in location_table.items():
        if (data.category == "enemy" or data.category == "pgenemy") and not options.cardsanity == CardSanity.option_all:
            continue
        if (data.category == "boss" or data.category == "pgboss") and options.cardsanity == CardSanity.option_false:
            continue
        if data.category == "relax" and options.shuffle_relax == RelaxRankNeedsPass.option_false:
            continue
        if data.category == "fishing" and options.shuffle_fish_mission == ShuffleFishingMissions.option_false:
            continue
        if data.category == "aquarium" and options.aqariumsanity == AquariumSanity.option_false:
            continue
        if data.category[:2] == "pg" and options.ending_goal == EndingGoal.option_fake_ending:
            continue
        if data.region == "Heaven" and options.ending_goal == EndingGoal.option_marisa_kirisame:
            continue
        if (data.region == "Post Game" or data.category[:2] == "pm") and options.ending_goal != EndingGoal.option_all_completion_bonus:
            continue
        if data.region == "Levelsanity" and options.levelsanity != LevelSanity.option_true:
            continue

        regions[data.region].locations.append(name)

    for name, data in event_location_table.items():
        regions[data.region].locations.append(name)

    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))
        
    for name, data in regions.items():
        connect_regions(multiworld, player, name, data)

def create_region(multiworld: MultiWorld, player: int, name: str, data: UT2RegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = UT2Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    return region
    
def connect_regions(multiworld: MultiWorld, player: int, source: str, data: UT2RegionData, rule=None):
    for _, target in enumerate(data.exits):
        sourceRegion = multiworld.get_region(source, player)
        targetRegion = multiworld.get_region(target, player)
        sourceRegion.connect(targetRegion, rule=rule)