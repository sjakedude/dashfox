# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import subprocess
import json
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


def read_json():
    with open("xbox_config.json", 'r') as file:
        data = json.load(file)
    return data


class Syncer:

    def __init__(self, profile, game_names):
        self.config = read_json()
        self.profile = self.verify_profile(profile)
        self.game_names = self.verify_game_names(game_names)
        self.xboxs = self.get_xbox_ips()
        self.metadata = self.create_metadata_dict()


    def verify_profile(self, profile):
        try:
            self.config["xbox_profiles"][profile]
        except KeyError:
            print(f"Profile {profile} not supported")


    def verify_game_names(self, game_names):
        games = game_names.split("|")
        for game in games:
            try:
                self.config["xbox_games"][game]
            except KeyError:
                print(f"Game {game} not supported")
        return games
        

    def create_metadata_dict(self):
        metadata = {}
        for xbox in self.xboxs:
            metadata[xbox] = {}
            for game_name in self.game_names:
                metadata[xbox][game_name] = None
        return metadata

    def get_xbox_ips(self):
        xboxs = []
        for key in self.config["xbox_ips"]:
            xboxs.append(self.config["xbox_ips"][key])
        return xboxs

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
            for game in self.game_names:
                output = str(
                    check_output(
                        f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_metadata.bat {xbox} {self.profile} {self.config["xbox_games"][game]["title_id"]}",
                        shell=True,
                    )
                )
                last_modified = self.get_last_modified(output, game)
                self.metadata[xbox][game] = last_modified
        print(self.metadata)

        # xbox_with_latest_save = self.get_latest_save_file()
        # self.upload_latest_save_file(xbox_with_latest_save)
