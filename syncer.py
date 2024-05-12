# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import subprocess
from subprocess import check_output
from subprocess import CalledProcessError

# Gamertag ID
XBOX_PROFILE_ID = "E00000E4D88A136A"

# Console IP addresses
JASPER_RGH_IP = "192.168.0.233"
OFFICE_RGH_IP = "192.168.0.234:21"

# Game Title ID and Save File Name
GAME_TITLE_ID = "4D53082D"
GAME_SAVE_NAME = "Gears2Checkpoint"


class Syncer:

    def __init__(self, console_type):
        self.console_type = console_type
        self.xboxs = [JASPER_RGH_IP]
        self.metadata = {JASPER_RGH_IP: None, OFFICE_RGH_IP: None}


    def get_last_modified(self, response):
        tokens = response.split("-rwxrwxrwx")
        for token in tokens:
            print("TOKEN")
            print(token)
        metadata_line = token[1]
        date = token[1].split("Gears2Checkpoint")[0]
        print(date)
        new_tokens = date.split(" ")
        for new_token in new_tokens:
            print("new token")
            print(new_token)
        year = new_tokens[-1]
        day = new_tokens[-2]
        month = new_tokens[-3]
        print(f"Last Updated: {month} {day} {year}")
        print("asdf")


    def sync_saves(self):
        # connect to each xbox and retrieve metadata for game
        for xbox in self.xboxs:
            print("HI")
            output = str(
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_metadata.bat {xbox} {XBOX_PROFILE_ID} {GAME_TITLE_ID}",
                    shell=True,
                )
            )
            print(output)
            print(type(output))
            last_modified = self.get_last_modified(output)
