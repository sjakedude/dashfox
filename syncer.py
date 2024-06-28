# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import json
import re
from subprocess import check_output
from datetime import datetime
import time

def read_json():
    with open("xbox_config.json", 'r') as file:
        data = json.load(file)
    return data

class Syncer:

    def __init__(self, profile, game):
        self.config = read_json()
        self.profile = self.verify_profile(profile)
        self.game = self.verify_game(game)
        self.xboxs = self.get_xbox_ips()
        self.metadata = self.create_metadata_dict()


    def verify_profile(self, profile):
        try:
            return self.config["xbox_profiles"][profile]
        except KeyError:
            print(f"Profile {profile} not supported")


    def verify_game(self, game):
        try:
            self.config["xbox_games"][game]
        except KeyError:
            print(f"Game {game} not supported")
        return game
        

    def create_metadata_dict(self):
        metadata = {}
        for xbox in self.xboxs:
            metadata[xbox] = {self.game: {"last_updated": None, "file_names": []}}
        return metadata

    def get_xbox_ips(self):
        xboxs = []
        for key in self.config["xbox_ips"]:
            xboxs.append(self.config["xbox_ips"][key])
        return xboxs


        


    def get_max_last_modified(self, response):
        lines = response.split("\\n")
        files = []
        for line in lines:
            if "-rwxrwxrwx" in line:
                files.append(line.replace("\xa0", " "))
        timestamps = []
        file_names = []
        for file in files:
            print(file)
            tokens = file.split(" ")
            print(tokens)
            month = tokens[13]
            day = tokens[14]
            year_or_time = tokens[15]
            filename = ""
            for file_name_part in tokens[16::]:
                filename = filename + file_name_part + " "
            filename =  filename.strip().replace("\\r", "")
            if ":" in year_or_time:
                timestamp_str = f"{month} {day} {datetime.now().year} {year_or_time}"
                timestamp_format = "%b %d %Y %H:%M"
            else:
                timestamp_str = f"{month} {day} {year_or_time}"
                timestamp_format = "%b %d %Y"
            parsed_timestamp = datetime.strptime(timestamp_str, timestamp_format)
            timestamps.append(parsed_timestamp)    
            file_names.append(filename)
        return max(timestamps), file_names

    def purge_old_saves(self):
        check_output(
                f"Z:\Private\conecommons\scripts\\rom_sync\\purge_old_saves.bat {self.profile} {self.config['xbox_games'][self.game]['title_id']}",
                shell=True,
            )
        print("Old saves deleted from NAS")

    def get_latest_save_files(self):
        xbox_with_latest_save = None
        latest_date = None
        for xbox in self.metadata:
            date = self.metadata[xbox][self.game]["last_updated"]
            if not latest_date:
                latest_date = date
                xbox_with_latest_save = xbox
            if latest_date < date:
                xbox_with_latest_save = xbox
        print(f"Xbox with latest timestamp determined as: {xbox_with_latest_save}")
        print("Deleting old saves")
        self.purge_old_saves()
        for file in self.metadata[xbox_with_latest_save][self.game]["file_names"]:
            print(f"Downloading {file} from xbox")
            check_output(
                f"Z:\Private\conecommons\scripts\\rom_sync\\download_xbox_file.bat {xbox_with_latest_save} {self.profile} {self.config['xbox_games'][self.game]['title_id']} \"{file}\"",
                shell=True,
            )
            print(f"Latest save file {file} downloaded from {xbox_with_latest_save}")
        return xbox_with_latest_save

    def upload_latest_save_files(self, xbox_with_latest_save):
        for xbox in self.metadata:
            if xbox != xbox_with_latest_save:
                for file_name in self.metadata[xbox][self.game]["file_names"]:
                    check_output(
                        f"Z:\Private\conecommons\scripts\\rom_sync\\delete_xbox_saves.bat {xbox} {self.profile} {self.config['xbox_games'][self.game]['title_id']} {file_name}",
                        shell=True,
                    )
                    print(f"Deleted save file {file_name} on {xbox}")
                print("About to upload new files to xbox")
                for file_name in self.metadata[xbox_with_latest_save][self.game]["file_names"]:
                    check_output(
                        f"Z:\Private\conecommons\scripts\\rom_sync\\upload_xbox_file.bat {xbox} {self.profile} {self.config['xbox_games'][self.game]['title_id']} {file_name}",
                        shell=True,
                    )
                    print(f"Latest save file {file_name} uploaded to {xbox}")

    def sync_saves(self):
        # connect to each xbox and retrieve metadata for game
        for xbox in self.xboxs:
            output = str(
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_xbox_metadata.bat {xbox} {self.profile} {self.config['xbox_games'][self.game]['title_id']}",
                    shell=True,
                )
            )
            last_modified, file_names = self.get_max_last_modified(output)
            self.metadata[xbox][self.game]["last_updated"] = last_modified
            self.metadata[xbox][self.game]["file_names"] = file_names
        print(self.metadata)

        xbox_with_latest_save = self.get_latest_save_files()
        self.upload_latest_save_files(xbox_with_latest_save)
        print("Saves Synced!")
