from typing import List, ClassVar

from BaseClasses import Tutorial, Region, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import UT2Item, UT2ItemData, event_item_table, get_items_by_category, item_table
from .Locations import UT2Location, location_table
from .Options import UT2Options, ProgLokeyKey, RelaxRankNeedsPass, ShuffleFishingMissions, EndingGoal, EarlyBeach, StartingCharacter, LevelSanity
from .Regions import create_regions
from .Rules import set_rules
from .ut_map.map_page_index import map_page_index


class UT2Web(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Undertale 2 Randomizer on your computer.",
        "English",
        "en_Undertale2.md",
        "setup/en",
        ["studkid"]
    )]

class UT2World(World):
    """
    UNDERTALE II: Revenge of the Robots is the new awesome sequel to UNDERTALE everyone has been talking about for the past few decades. It's totally not a FANGAME OR ANYTHING. 
    """
    game = "Undertale 2"
    options_dataclass = UT2Options
    options: UT2Options
    topology_present = False
    required_client_version = (0, 5, 0)
    web = UT2Web()
    item_name_groups = {
        "Party": {name for name, data in item_table.items() if data.category == "party"},
        "Head Armor": {name for name, data in item_table.items() if data.category == "head"},
        "Body Armor": {name for name, data in item_table.items() if data.category == "body"},
        "Eyewear": {name for name, data in item_table.items() if data.category == "eyewear"},
        "Trinket": {name for name, data in item_table.items() if data.category == "trinket"},
        "Weapon": {name for name, data in item_table.items() if data.category == "weapon"},
        "Code Thing": {name for name, data in item_table.items() if data.category == "pgcode"},
        "Completion Items": {name for name, data in item_table.items() if data.category == "pgcompletion"},
        "Skills": {name for name, data in item_table.items() if data.category == "skill" or data.category == "lvskill"},
    }

    tracker_world: ClassVar = {
        "map_page_folder": "ut_map",
        "map_page_maps": "maps.json",
        "map_page_locations": "locations.json",
        "map_page_setting_key": "{player}_{team}_undertale2_area",
        "map_page_index": map_page_index
    }

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}

    def create_items(self):
        item_pool: List[UT2Item] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        starting_char = None

        if self.options.shuffle_relax == RelaxRankNeedsPass.option_false:
            item_table["Relax Pass"] = UT2ItemData("misc prog", 311, ItemClassification.progression, 1)
            self.multiworld.push_precollected(self.create_item("Relax Pass Off"))

        if self.options.shuffle_fish_mission == ShuffleFishingMissions.option_false:
            self.multiworld.push_precollected(self.create_item("Fishing Mission Off"))

        if self.options.levelsanity == LevelSanity.option_true:
            self.multiworld.push_precollected(self.create_item("Levelsanity"))

        if self.options.early_beach == EarlyBeach.option_item:
            item_table["Honeycomb Beach Access"]._replace(max_quantity = 1)

        if self.options.ending_goal == EndingGoal.option_fake_ending:
            self.multiworld.push_precollected(self.create_item("Fake Ending Goal"))
        elif self.options.ending_goal == EndingGoal.option_marisa_kirisame:
            self.multiworld.push_precollected(self.create_item("Marisa Kirisame Goal"))
        elif self.options.ending_goal == EndingGoal.option_true_ending:
            self.multiworld.push_precollected(self.create_item("True Ending Goal"))
        elif self.options.ending_goal == EndingGoal.option_all_completion_bonus:
            self.multiworld.push_precollected(self.create_item("All Completion Bonus Goal"))

        if self.options.starting_character == StartingCharacter.option_frisk:
            self.multiworld.push_precollected(self.create_item("Frisk"))
            starting_char = "Frisk"
        elif self.options.starting_character == StartingCharacter.option_fabio:
            self.multiworld.push_precollected(self.create_item("Fabio"))
            starting_char = "Fabio"
        elif self.options.starting_character == StartingCharacter.option_sans:
            self.multiworld.push_precollected(self.create_item("sans"))
            starting_char = "sans"
        elif self.options.starting_character == StartingCharacter.option_nazrin:
            self.multiworld.push_precollected(self.create_item("Nazrin"))
            starting_char = "Nazrin"
        elif self.options.starting_character == StartingCharacter.option_eclaire:
            self.multiworld.push_precollected(self.create_item("Eclaire"))
            starting_char = "Eclaire"

        for name, data in item_table.items():
            quantity = data.max_quantity

            if data.category == "key" and self.options.progressive_lokey_key != ProgLokeyKey.option_false:
                continue
            elif data.category == "progkey" and self.options.progressive_lokey_key != ProgLokeyKey.option_true:
                continue

            if name == "Progressive Fishing Spot" and self.options.shuffle_fish_mission == ShuffleFishingMissions.option_false:
                continue

            if data.category[:2] == "pg" and self.options.ending_goal == EndingGoal.option_fake_ending:
                continue

            if (name == "Flynn" or name == "Otta" or name == "Nico" or name == "Nim") and self.options.ending_goal != EndingGoal.option_all_completion_bonus:
                continue

            if name == starting_char:
                continue

            if name == "Honeycomb Beach Access" and self.options.early_beach != EarlyBeach.option_item:
                continue

            if data.category == "lvskill" and self.options.levelsanity != LevelSanity.option_true:
                continue

            item_pool += [self.create_item(name) for _ in range(0, quantity)]

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("filler")
        weights = [data.weight for data in fillers.values()]
        return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def create_item(self, name: str) -> UT2Item:
        data = item_table[name]
        return UT2Item(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> UT2Item:
        data = event_item_table[name]
        return UT2Item(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
        self._place_events()
        if self.options.progressive_lokey_key == ProgLokeyKey.option_vanilla:
            self.multiworld.get_location("Ruins - Lake Gold Key", self.player).place_locked_item(
                            self.create_item("Gold Key"))
            self.multiworld.get_location("Ruins - Lake Silver Key", self.player).place_locked_item(
                            self.create_item("Silver Key"))
            self.multiworld.get_location("Ruins - Lake Bronze Key", self.player).place_locked_item(
                            self.create_item("Bronze Key"))
            
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def _place_events(self):
        self.multiworld.get_location("Lancer Encounter", self.player).place_locked_item(
            self.create_event("Lancer Encountered"))
        
        self.multiworld.get_location("Hotden Reached", self.player).place_locked_item(
            self.create_event("Hotden Reached"))
        
        self.multiworld.get_location("Cirno Defeated", self.player).place_locked_item(
            self.create_event("Prison Destroyed"))
        
        self.multiworld.get_location("Tutariel Defeated", self.player).place_locked_item(
            self.create_event("Decision Chosen"))
        
        self.multiworld.get_location("Fake Ending", self.player).place_locked_item(
            self.create_event("Pope Plays Undertale 2"))
        
        self.multiworld.get_location("Lulliby Setting", self.player).place_locked_item(
            self.create_event("Lulliby Active"))
        
        self.multiworld.get_location("Marisa Battle", self.player).place_locked_item(
            self.create_event("Marisa Defeated"))
        
        self.multiworld.get_location("Seraph Battle", self.player).place_locked_item(
            self.create_event("Seraph Defeated"))
        
        self.multiworld.get_location("Spark Battle", self.player).place_locked_item(
            self.create_event("Spark Defeated"))
        
        self.multiworld.get_location("Travis Battle", self.player).place_locked_item(
            self.create_event("Travis Defeated"))
        
        self.multiworld.get_location("Froguelass Battle", self.player).place_locked_item(
            self.create_event("Froguelass Defeated"))
        
        self.multiworld.get_location("Ra Men Battle", self.player).place_locked_item(
            self.create_event("Ra Men Defeated"))
        
    def fill_slot_data(self):
        options_dict = self.options.as_dict("ending_goal", casing="camel")
        return {
            **options_dict,
        }
