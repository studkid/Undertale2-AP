# Undertale 2 Archipelago Randomizer
This is a mod for [Undertale 2](https://pep.itch.io/undertale-2) that adds support for the [Archipelago multiworld randomizer](https://archipelago.gg/).  This project uses EggSlashEther's [RPGMaker-VX-AAce-AP](https://github.com/EggSlashEther/RPGMaker-VX-Ace-AP) plugin to handle connection to an AP server.

For more information, refer to the following:
[Setup Guide](https://github.com/studkid/Undertale2-AP/blob/main/World/docs/setup_en.md)
[Game Page](https://github.com/studkid/Undertale2-AP/blob/main/World/docs/en_undertale2.md)

# Known Issues
- Generation will fail if goal is set to `marisa_kirisame` or `true_ending` while `shuffle_fish_mission` is false and `aquariumsanity` is true
- `all_completion_bonus` goal sometimes gens unbeatable seeds.
- If you game over/return to the main menu, you will need to do a full game restart to be able to reconnect
- If the room port ever changes, you will need to restart your save file to continue play (unless you know your way around a hex editor to edit the port in the save file yourself)
