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


    def convert_month(month):
        if month == "Jan":
            return 1
        elif month == "Feb":
            return 2
        elif month == "Mar":
            return 3
        elif month == "Apr":
            return 4
        elif month == "May":
            return 5
        elif month == "Jun":
            return 6
        elif month == "Jul":
            return 7
        elif month == "Aug":
            return 8
        elif month == "Sep":
            return 9
        elif month == "Oct":
            return 10
        elif month == "Nov":
            return 11
        elif month == "Dec":
            return 12


    def get_last_modified(self, response, save_file_name):
        tokens = response.split("-rwxrwxrwx")
        metadata_line = tokens[1]
        date = tokens[1].split(save_file_name)[0]
        metadata_line_tokens = date.split(" ")
        year = metadata_line_tokens[-2]
        day = metadata_line_tokens[-3]
        month = convert_month(metadata_line_tokens[-4])
        print(f"Last Updated: {month}/{day}/{year}")


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
