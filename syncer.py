# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import json
from subprocess import check_output

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
            self.config["xbox_profiles"][profile]
        except KeyError:
            print(f"Profile {profile} not supported")


    def verify_game(self, game):
        try:
            self.config["xbox_games"][game]
        except KeyError:
            print(f"Game {game} not supported")
        

    def create_metadata_dict(self):
        metadata = {}
        for xbox in self.xboxs:
            metadata[xbox] = {self.game: None}
        return metadata

    def get_xbox_ips(self):
        xboxs = []
        for key in self.config["xbox_ips"]:
            xboxs.append(self.config["xbox_ips"][key])
        return xboxs


    def get_last_modified(self, response):
        epoch_ts = response.split("date -r . +%s \r\n")[1].split("\r\nquit")[0]
        return epoch_ts

    def get_latest_save_file(self):
        xbox_with_latest_save = None
        latest_date = None
        for xbox in self.metadata:
            date = self.metadata[xbox][self.game]
            if not latest_date:
                latest_date = date
                xbox_with_latest_save = xbox
            if latest_date < date:
                xbox_with_latest_save = xbox
        check_output(
            f"Z:\Private\conecommons\scripts\\rom_sync\\download_xbox_file.bat {xbox_with_latest_save} {self.profile} {self.config['xbox_games'][self.game]['title_id']}",
            shell=True,
        )
        print(f"Latest save file downloaded from {xbox_with_latest_save}")
        return xbox_with_latest_save

    def upload_latest_save_file(self, xbox_with_latest_save):
        for xbox in self.metadata:
            if xbox != xbox_with_latest_save:
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\upload_xbox_file.bat {xbox} {self.profile} {self.config['xbox_games'][self.game]['title_id']}",
                    shell=True,
                )
                print(f"Latest save file uploaded to {xbox}")

    def sync_saves(self):
        # connect to each xbox and retrieve metadata for game
        for xbox in self.xboxs:
            output = str(
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_xbox_metadata.bat {xbox} {self.profile} {self.config['xbox_games'][self.game]['title_id']}",
                    shell=True,
                )
            )
            last_modified = self.get_last_modified(output)
            self.metadata[xbox][self.game] = last_modified
        print(self.metadata)

        # xbox_with_latest_save = self.get_latest_save_file()
        # self.upload_latest_save_file(xbox_with_latest_save)
