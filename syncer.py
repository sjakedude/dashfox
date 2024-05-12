# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import subprocess
from subprocess import check_output
from subprocess import CalledProcessError
from datetime import datetime

# Gamertag ID
XBOX_PROFILE_ID = "E00000E4D88A136A" # sjakedude

# Console IP addresses
JASPER_RGH_IP = "192.168.0.233"
OFFICE_RGH_IP = "192.168.0.234"

# Game Title ID and Save File Name
GAME_TITLE_ID = "425307D5"
GAME_SAVE_NAME = "Gears2Checkpoint"


class Syncer:

    def __init__(self, console_type):
        self.console_type = console_type
        self.xboxs = [JASPER_RGH_IP]
        self.metadata = {
            JASPER_RGH_IP: {GAME_SAVE_NAME: None},
            # OFFICE_RGH_IP: {GAME_SAVE_NAME: None},
        }

    def convert_month(self, month):
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
        print("RESSPONSE")
        print(response)
        tokens = response.split("-rwxrwxrwx")
        print("tokens")
        print(tokens)
        metadata_line = tokens[1]
        return "bla"
        date = tokens[1].split(save_file_name)[0]
        metadata_line_tokens = date.split(" ")
        year = metadata_line_tokens[-2]
        day = metadata_line_tokens[-3]
        month = self.convert_month(metadata_line_tokens[-4])
        return f"{month}/{day}/{year}"

    def get_latest_save_file(self):
        xbox_with_latest_save = None
        latest_date = None
        for xbox in self.metadata:
            date = datetime.strptime(self.metadata[xbox][GAME_SAVE_NAME], "%m/%d/%Y")
            if not latest_date:
                latest_date = date
                xbox_with_latest_save = xbox
            if latest_date < date:
                xbox_with_latest_save = xbox
        output = str(
            check_output(
                f"Z:\Private\conecommons\scripts\\rom_sync\\download_file.bat {xbox_with_latest_save} {XBOX_PROFILE_ID} {GAME_TITLE_ID} {GAME_SAVE_NAME} {self.console_type}",
                shell=True,
            )
        )
        print(f"Latest save file downloaded from {xbox_with_latest_save}")
        return xbox_with_latest_save

    def upload_latest_save_file(self, xbox_with_latest_save):
        for xbox in self.metadata:
            if xbox != xbox_with_latest_save:
                output = str(
                    check_output(
                        f"Z:\Private\conecommons\scripts\\rom_sync\\upload_file.bat {xbox} {XBOX_PROFILE_ID} {GAME_TITLE_ID} {GAME_SAVE_NAME} {self.console_type}",
                        shell=True,
                    )
                )
                print(f"Latest save file uploaded to {xbox}")

    def sync_saves(self):
        # connect to each xbox and retrieve metadata for game
        for xbox in self.xboxs:
            output = str(
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_metadata.bat {xbox} {XBOX_PROFILE_ID} {GAME_TITLE_ID}",
                    shell=True,
                )
            )
            last_modified = self.get_last_modified(output, GAME_SAVE_NAME)
            self.metadata[xbox][GAME_SAVE_NAME] = last_modified
        print(self.metadata)

        # xbox_with_latest_save = self.get_latest_save_file()
        # self.upload_latest_save_file(xbox_with_latest_save)
