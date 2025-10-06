from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionSet, PerGameCommonOptions

from dataclasses import dataclass

class EndingGoal(Choice):
    """
    Choose which ending you want for your goal
    Fake Ending - Cross the border to Ashburg and seeing the credits.
    Marisa Kirisame - Defeat Marisa Kirisame.
    True Ending - Defeat Seriph and leave Itoi Island
    All Completion Bonus - Finish the True Ending with 13/13 Ending bonuses
    """
    display_name = "Ending Goal"
    option_fake_ending = 0
    option_marisa_kirisame = 1
    option_true_ending = 2
    option_all_completion_bonus = 3
    default = 0

class ProgMonkKey(Choice):
    """
    Makes the gold, silver, bronze and monk key progressive.
    If Monk Key Only, the gold, silver and bronze keys will be vanilla.
    """
    display_name = "Progressive Monk Key"
    option_false = 0
    option_true = 1
    option_monk_key_only = 2
    default = 2

class RelaxRankNeedsPass(DefaultOnToggle):
    """
    Adds 6 more Relax Passes into the pool.  A relax pass will be consumed on each relax battle victory.
    (Recommended to be on until combat logic is done)
    """
    display_name = "Relax Rank needs Passes"

class ShuffleFishingMissions(Toggle):
    """
    Turns fishing missions into locations.  Progressive Fishing Spot is required
    to access new areas.
    """
    display_name = "Shuffle Fishing Missions"

class CardSanity(Choice):
    """
    Turns card drops into locations. It's a 1/50 chance drop from most enemies.
    Cards that are normally found in chests are instead shuffled into the pool
    (You will need to interact with the card in your inventory to send the location)
    """
    display_name = "Cardsanity"
    option_false = 0
    option_bosses_only = 1
    option_all = 2

class RequireNazrin(DefaultOnToggle):
    """
    Require Nazrin and Mousey Help to obtain non guarenteed enemy cards
    Does nothing if cardsanity is not set to all
    """
    display_name = "Require Nazrin"

class AquariumSanity(Toggle):
    """
    Turns Aquarium Donations into locations
    """
    display_name = "Aquariumsanity"

@dataclass
class UT2Options(PerGameCommonOptions):
    ending_goal: EndingGoal
    progressive_monkkey: ProgMonkKey
    shuffle_relax: RelaxRankNeedsPass
    shuffle_fish_mission: ShuffleFishingMissions
    cardsanity: CardSanity
    require_nazrin: RequireNazrin
    aqariumsanity: AquariumSanity
