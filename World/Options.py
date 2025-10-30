from Options import Choice, Toggle, DefaultOnToggle, PerGameCommonOptions

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
    default = 1

class StartingCharacter(Choice):
    """
    Selects your starting party member.
    May cause issues with some events, use with caution.
    """
    display_name = "Starting Character"
    option_frisk = 0
    option_fabio = 1
    option_sans = 2
    option_nazrin = 3
    option_eclaire = 4
    default = 0

class ProgLokeyKey(Choice):
    """
    Makes the gold, silver, bronze progressive.
    Note: shuffling these could cause you to get stuck early for a very long time.
    """
    display_name = "Progressive Lokey Key"
    option_false = 0
    option_true = 1
    option_vanilla = 2
    default = 2

class EarlyBeach(Choice):
    """
    Determines if the warp to Honeycomb Beach should be unlocked early.  This leads to a far less restrictive start.
    Jinx and Punchbuggy will not be able to be fought until after the prison sequence.
    If set to Item, the warp will instead be shuffled behind an item.
    """
    display_name = "Early Beach Access"
    option_false = 0
    option_true = 1
    option_item = 2
    default = 0

class RelaxRankNeedsPass(DefaultOnToggle):
    """
    Adds 6 more Relax Passes into the pool.  A relax pass will be consumed on each relax battle victory.
    (Recommended to be on until combat logic is done)
    """
    display_name = "Relax Rank needs Passes"

class ShuffleFishingMissions(DefaultOnToggle):
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

class RequireNegotiation(DefaultOnToggle):
    """
    Require ability to use negotiation to obtain non guarenteed enemy cards
    Requires Frisk, Nazrin and Mouse in your Pocket
    Does nothing if cardsanity is not set to all
    """
    display_name = "Require Negotiation"

class AquariumSanity(Toggle):
    """
    Turns Aquarium Donations into locations
    """
    display_name = "Aquariumsanity"

class LevelSanity(Toggle):
    """
    Adds level ups per party member as a location.
    Additionally shuffles level up moves into the pool.
    """
    display_name = "Levelsanity"

@dataclass
class UT2Options(PerGameCommonOptions):
    ending_goal: EndingGoal
    starting_character: StartingCharacter
    progressive_lokey_key: ProgLokeyKey
    early_beach: EarlyBeach
    shuffle_relax: RelaxRankNeedsPass
    shuffle_fish_mission: ShuffleFishingMissions
    cardsanity: CardSanity
    require_negotiation: RequireNegotiation
    aqariumsanity: AquariumSanity
    levelsanity: LevelSanity
