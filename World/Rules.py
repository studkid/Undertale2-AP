from typing import List
from BaseClasses import CollectionState, MultiWorld, Location, Region, Item
from .Options import UT2Options, CardSanity, RequireNazrin, AquariumSanity, ShuffleFishingMissions, RelaxRankNeedsPass, EndingGoal
from .Locations import location_table
from .MiscData import fish_data, fish_quests

enemy_locations: List[str] = []
boss_locations: List[str] = []

def has_all(state: CollectionState, player: int, items: List[str]) -> bool:
    for _, item in enumerate(items):
        if not state.has(item, player):
            return False
        
    return True

def party_count(state: CollectionState, player: int) -> int:
    party = ["Fabio", "sans", "Nazrin", "Eclaire"]
    count = 1

    for _, name in enumerate(party):
        if state.has(name, player):
            count += 1

        if count == 4:
            break

    return count

def can_beat_snopestablook(state: CollectionState, player: int) -> bool:
    return party_count(state, player) >= 2

def can_beat_swamp(state: CollectionState, player: int) -> bool:
    return party_count(state, player) >= 2

def can_beat_froguelass(state: CollectionState, player: int) -> bool:
    return party_count(state, player) >= 3

def can_beat_cirno(state: CollectionState, player: int) -> bool:
    return party_count(state, player) >= 4

def can_get_fish(state: CollectionState, name: str, player: int) -> bool:
    for _, region in enumerate(fish_data[name]):
        if state.can_reach(region, "Region", player):
            return True
        
    return False

def can_reach_cards(state: CollectionState, player: int, options: UT2Options) -> bool:
    if options.ending_goal != EndingGoal.option_all_completion_bonus:
        return False

    if options.cardsanity == CardSanity.option_all:
        for _, name in enumerate(enemy_locations):
            if not state.can_reach(name, "Location", player):
                return False
            
    if options.cardsanity != CardSanity.option_false:
        for _, name in enumerate(boss_locations):
            if not state.can_reach(name, "Location", player):
                return False
            
    if not state.has_all(["#X ??? ??? ??? ???", "#-1 Death Metal", "#0 Placeholdio"], player):
        return False
    
    return True

def can_reach_fish(state: CollectionState, player: int) -> int:
    donations = 0
    
    for _, data in fish_data.items():
        for __, name in enumerate(data):
            if state.can_reach(name, "Region", player):
                donations += 1
                break

    return donations

def set_rules(multiworld: MultiWorld, player: int, options: UT2Options):
    for name, data in location_table.items():
        if data.category[:2] == "pg" and options.ending_goal == EndingGoal.option_fake_ending:
            continue
        if options.cardsanity != CardSanity.option_false and (data.category == "boss" or data.category == "pgboss"):
            boss_locations.append(name)
        elif options.cardsanity == CardSanity.option_all and (data.category == "enemy" or data.category == "pgenemy"):
            enemy_locations.append(name)
        
        if data.category == "dig":
            multiworld.get_location(name, player).access_rule = \
                lambda state: state.has("Joqua's Trowel", player)
            
    # Card Sanity -----------------------------------------------------------------------
    if options.cardsanity == CardSanity.option_all and options.require_nazrin == RequireNazrin.option_true:
        for _, name in enumerate(enemy_locations):
            if name == "#62 Seriph Card" and options.ending_goal != EndingGoal.option_all_completion_bonus:
                continue
            if name == "#59 Gilded☆Bingus Card":
                continue
            if name == "#11 Lancer Card":
                multiworld.get_location(name, player).access_rule = \
                    lambda state: state.has("Nazrin", player) and state.has("Lancer Encountered", player)
            if name == "#22 Angler Card":
                multiworld.get_location(name, player).access_rule = \
                    lambda state: state.has("Nazrin", player) and can_get_fish(state, "Angler", player)
            if name == "#23 Angeler Card":
                multiworld.get_location(name, player).access_rule = \
                    lambda state: state.has("Nazrin", player) and can_get_fish(state, "Angeler", player)
            
            multiworld.get_location(name, player).access_rule = \
                lambda state: state.has("Nazrin", player)
    elif options.cardsanity == CardSanity.option_all:
        multiworld.get_location("#11 Lancer Card", player).access_rule = \
            lambda state: state.has("Lancer Encountered", player)
        multiworld.get_location("#22 Angler Card", player).access_rule = \
            lambda state: can_get_fish(state, "Angler", player)
        multiworld.get_location("#23 Angeler Card", player).access_rule = \
            lambda state: can_get_fish(state, "Angeler", player)

    # Ruins -----------------------------------------------------------------------
    multiworld.get_entrance("Ruins Main -> Ruins Sewers", player).access_rule = \
        lambda state: state.has("Lucky Crowbar", player)
    multiworld.get_entrance("Ruins Main -> Scopestablook", player).access_rule = \
        lambda state: can_beat_snopestablook(state, player)
    multiworld.get_entrance("Ruins Lake -> Ruins Tree", player).access_rule = \
        lambda state: has_all(state, player, ["Gold Key", "Silver Key", "Bronze Key", "Progressive Monk Key"])\
                          or state.has("Progressive Key", player, 4)

    # Archives -----------------------------------------------------------------------
    multiworld.get_entrance("Archives Pit -> Archives Sewers", player).access_rule = \
        lambda state: state.has("Lucky Crowbar", player)
    multiworld.get_entrance("Archives Pit -> Archives Back", player).access_rule = \
        lambda state: state.has("Library Card", player)
    multiworld.get_entrance("Archives Pit -> Frogue Chamber", player).access_rule = \
        lambda state: (state.has("Progressive Monk Key", player, 2) or state.has("Progressive Key", player, 5)) and \
                       can_beat_froguelass(state, player)
    multiworld.get_location("Hotden - Paneton Gift", player).access_rule =\
        lambda state: state.has("Spark Defeated", player)
    
    # Swamp -----------------------------------------------------------------------
    multiworld.get_entrance("Ruins Tree -> Swamp", player).access_rule =\
        lambda state: state.has("Hotden Reached", player)
    multiworld.get_entrance("Swamp -> Spark Chamber", player).access_rule =\
            lambda state: state.has("Odd Key", player, 3)
    
    # Prison -----------------------------------------------------------------------
    multiworld.get_entrance("Hotden -> Prison Cells", player).access_rule =\
        lambda state: has_all(state, player, ["sans", "Anime catboy transformation potion"]) and \
                          (state.has("Progressive Monk Key", player, 2) or state.has("Progressive Key", player, 5))
    
    multiworld.get_location("Prison - Marylin Reward #1", player).access_rule =\
        lambda state: has_all(state, player, ["Puzzle Key"])
    multiworld.get_location("Prison - Marylin Reward #2", player).access_rule =\
        lambda state: has_all(state, player, ["Puzzle Key"])
    if options.cardsanity != CardSanity.option_false:
        multiworld.get_location("#20 Marylin Card", player).access_rule =\
            lambda state: has_all(state, player, ["Puzzle Key"])
    
    multiworld.get_entrance("Prison Cells -> Prison Kitchen", player).access_rule =\
        lambda state: state.has("Prison Key", player)
    
    multiworld.get_entrance("Prison Kitchen -> Prison Office", player).access_rule =\
        lambda state: can_beat_cirno(state, player)
    
    # Beach -----------------------------------------------------------------------
    multiworld.get_entrance("Prison Office -> Beach Entry", player).access_rule =\
        lambda state: state.has("Prison Destroyed", player)    
            
    multiworld.get_entrance("Beach Entry -> Beach Relax 1", player).access_rule =\
        lambda state: state.has("Relax Pass", player, 1)
    if options.shuffle_relax == RelaxRankNeedsPass.option_true:
        multiworld.get_entrance("Beach Relax 1 -> Beach Relax 2", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 2)
        multiworld.get_entrance("Beach Relax 2 -> Beach Relax 3", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 3)
        multiworld.get_entrance("Beach Relax 3 -> Beach Relax 4", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 4)
        multiworld.get_entrance("Beach Relax 4 -> Beach Relax 5", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 5)
        multiworld.get_entrance("Beach Relax 5 -> Beach Relax 6", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 6)
        multiworld.get_entrance("Beach Relax 6 -> Beach Relax 7", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 7)
        multiworld.get_entrance("Beach Relax 7 -> Beach Relax 8", player).access_rule =\
            lambda state: state.has("Relax Pass", player, 8) and (state.has("Ice crystals", player) or state.has("Nazrin", player))
    else:
        multiworld.get_entrance("Beach Relax 7 -> Beach Relax 8", player).access_rule =\
            lambda state: state.has("Ice crystals", player) or state.has("Nazrin", player) # Nazrin for crafting a New Year's Eve Bomb
    
    multiworld.get_entrance("Beach Entry -> Greenhorn Shore", player).access_rule =\
        lambda state: state.has("Membership Card", player)
    if options.shuffle_fish_mission == ShuffleFishingMissions.option_true:
        multiworld.get_entrance("Greenhorn Shore -> Breadcrumb Bay", player).access_rule =\
            lambda state: state.has("Progressive Fishing Spot", player)
        multiworld.get_entrance("Breadcrumb Bay -> Melonbread Cove", player).access_rule =\
            lambda state: state.has("Progressive Fishing Spot", player, 3)
        multiworld.get_entrance("Melonbread Cove -> Pudding", player).access_rule =\
            lambda state: state.has("Progressive Fishing Spot", player, 5)
        multiworld.get_location("Beach - Piss and Shit FM HQ", player).access_rule =\
            lambda state: state.has("Progressive Fishing Spot", player, 6)
        multiworld.get_entrance("Greenhorn Shore -> Rust Gear Gulf", player).access_rule =\
            lambda state: state.has("Rust Ticket", player) and state.has("Progressive Fishing Spot", player, 4)
        multiworld.get_entrance("Greenhorn Shore -> Chemical Waste Zone", player).access_rule =\
            lambda state: state.has("Waste Ticket", player) and state.has("Progressive Fishing Spot", player, 4)
        multiworld.get_entrance("Greenhorn Shore -> Big Bone Bay", player).access_rule =\
            lambda state: state.has("Bone Ticket", player) and state.has("Progressive Fishing Spot", player, 4)
        multiworld.get_entrance("Greenhorn Shore -> Stardrop Tree", player).access_rule =\
            lambda state: state.has("Star Ticket", player) and state.has("Progressive Fishing Spot", player, 4)     
        multiworld.get_location("Beach - Greenhorn Shore Chest", player).access_rule =\
        lambda state: state.has("Progressive Fishing Spot", player, 2)  
        
    else:    
        multiworld.get_entrance("Greenhorn Shore -> Rust Gear Gulf", player).access_rule =\
            lambda state: state.has("Rust Ticket", player)
        multiworld.get_entrance("Greenhorn Shore -> Chemical Waste Zone", player).access_rule =\
            lambda state: state.has("Waste Ticket", player)
        multiworld.get_entrance("Greenhorn Shore -> Big Bone Bay", player).access_rule =\
            lambda state: state.has("Bone Ticket", player)
        multiworld.get_entrance("Greenhorn Shore -> Stardrop Tree", player).access_rule =\
            lambda state: state.has("Star Ticket", player)
    
    multiworld.get_location("Beach - Melonbread Cove Chest", player).access_rule =\
        lambda state: can_get_fish(state, "Rubber Duckie", player)
    multiworld.get_location("Beach - Pudding Pond Can Trade", player).access_rule =\
        lambda state: can_get_fish(state, "Empty Can", player)
    multiworld.get_location("Stardrop Tree - Shyren Pisces Trade Chest", player).access_rule =\
        lambda state: state.can_reach("Big Bone Bay - Shyren Undyne Jr Trade", "Location", player)
    multiworld.get_location("Big Bone Bay - Shyren Undyne Jr Trade", player).access_rule =\
        lambda state: state.can_reach("Chemical Waste Zone - Shyren Pagliacci Chest", "Location", player)
    multiworld.get_location("Beach - Eclaire", player).access_rule =\
        lambda state: can_get_fish(state, "Taiyaki", player)
    multiworld.get_location("Beach - Helper Mimic Cave", player).access_rule = \
                    lambda state: state.has("Joqua's Trowel", player)
        
    if options.aqariumsanity == AquariumSanity.option_true:
        for name, data in fish_data.items():
            if data[0] == "Heaven" and options.ending_goal < 2:
                continue
            if data[0] == "Flowey Room" and options.ending_goal != EndingGoal.option_all_completion_bonus:
                continue
            if name == "Wrangler" and options.ending_goal != EndingGoal.option_all_completion_bonus:
                multiworld.get_location("Aquarium - " + name, player).access_rule =\
                    lambda state: can_get_fish(state, name, player) and can_reach_fish(state, player) >= 37
            
            multiworld.get_location("Aquarium - " + name, player).access_rule =\
                lambda state: can_get_fish(state, name, player)
            
    if options.shuffle_fish_mission == ShuffleFishingMissions.option_true:
        for i, name in enumerate(fish_quests):
            multiworld.get_location("Beach - Fishing Mission " + str(i + 1), player).access_rule =\
                lambda state: can_get_fish(state, name, player)
            
    multiworld.get_entrance("Beach Entry -> Miku Zone", player).access_rule =\
        lambda state: state.has("Vocal Key", player)
    
    # Toriel ------------------------------------------------------------------------------
    multiworld.get_entrance("Toriel House -> Toriel Roof", player).access_rule =\
        lambda state: state.has("Tutariel Key", player, 3)
    multiworld.get_entrance("Toriel House -> Mario Zone", player).access_rule =\
        lambda state: state.has("Red Coin", player, 8) and state.has("Decision Chosen", player)
    
    # Exit ------------------------------------------------------------------------------
    multiworld.get_entrance("Beach Post Boss -> Exit", player).access_rule =\
        lambda state: state.has("Decision Chosen", player)
    multiworld.get_entrance("Exit -> Exit Back", player).access_rule =\
        lambda state: state.has("Fake Passport", player)
    
    # Post Game ------------------------------------------------------------------------------
    if options.ending_goal != EndingGoal.option_fake_ending:
        multiworld.get_location("Toriel's House - Hallway Keycap", player).access_rule =\
            lambda state: state.has("Pope Plays Undertale 2", player)
        multiworld.get_location("Toriel's House - Your Room Keycap", player).access_rule =\
            lambda state: state.has("Pope Plays Undertale 2", player)
        multiworld.get_location("Toriel's House - Kitchen Keycap", player).access_rule =\
            lambda state: state.has("Pope Plays Undertale 2", player)
        multiworld.get_location("Ashburg - Nitori Gift", player).access_rule =\
            lambda state: state.has("Lulliby Active", player)
        
        multiworld.get_entrance("Toriel House -> Toriel Basement", player).access_rule =\
            lambda state: state.has("Numpad Keycap", player, 3)
        multiworld.get_entrance("Toriel Roof -> Server", player).access_rule =\
            lambda state: state.has("Mtech Brainlinq", player)
        multiworld.get_entrance("Server -> Server Settings", player).access_rule =\
            lambda state: has_all(state, player, ["38384201", "37482826", "38383838", "38421037", "11092696", "42042142", "83229978", "62828473", "80784838"])
        
        # Warehouse
        multiworld.get_entrance("Landing -> Warehouse", player).access_rule =\
            lambda state: has_all(state, player, ["Empty Gun", "Gun", "Lulliby Active"])
        multiworld.get_entrance("Warehouse -> Marisa Hall", player).access_rule =\
            lambda state: has_all(state, player, ["Lullaby Bells", "Lullaby Sword", "Lullaby Helmet"])
        multiworld.get_location("Warehouse - Patchmare Trade", player).access_rule =\
            lambda state: state.has("Mimic's adieu", player, 2)
        multiworld.get_location("Warehouse - Froguelass Gift", player).access_rule =\
            lambda state: state.has("Froguelass Defeated", player)
        
        multiworld.get_entrance("Exit -> Flowey Room", player).access_rule =\
            lambda state: can_reach_cards(state, player, options)
        
        multiworld.get_location("Read Bergo's Shopping List", player).access_rule =\
            lambda state: state.has("Bergo's Shopping List", player)
    
    # Win Condition -----------------------------------------------------------------------
    if options.ending_goal == EndingGoal.option_fake_ending:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Fake Ending", "Location", player)
    elif options.ending_goal == EndingGoal.option_marisa_kirisame:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Marisa Battle", "Location", player)
    elif options.ending_goal == EndingGoal.option_true_ending:
        multiworld.completion_condition[player] = lambda state: state.can_reach("Seraph Battle", "Location", player)
    elif options.ending_goal == EndingGoal.option_all_completion_bonus:
        if options.shuffle_fish_mission == ShuffleFishingMissions.option_true:
            multiworld.completion_condition[player] =\
                lambda state: state.can_reach("Beach - Fishing Mission 11", "Location", player) and \
                              can_reach_fish(state, player) == 38 and \
                              state.has_all(["Eclaire", "Grindy", "Spark Defeated", "Travis Defeated", "Wishgem", "Petsigrabber",
                                             "Flynn", "Otta", "Nico", "Nim", "Bergo's Shopping List", "Ra Men Defeated", "Seraph Defeated"], player)
        else:
            multiworld.completion_condition[player] =\
                lambda state: can_reach_fish(state, player) == 38 and \
                              state.has_all(["Eclaire", "Grindy", "Spark Defeated", "Travis Defeated", "Wishgem", "Petsigrabber",
                                             "Flynn", "Otta", "Nico", "Nim", "[Human]", "Ra Men Defeated", "Seraph Defeated"], player)
                          
    