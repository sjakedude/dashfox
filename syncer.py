# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

XBOX_PROFILE_ID = "E00000E4D88A136A"

JASPER_RGH_IP = "192.168.0.233"
OFFICE_RGH_IP = "192.168.0.234"

GAME_TITLE_ID = "4D53082D"
GAME_SAVE_NAME = "Gears2Checkpoint"


class Syncer:

    def __init__(self, console_type):
        self.console_type = console_type

    def sync_saves(self):
        # connect to each xbox and retrieve metadata for game
        xboxs = [JASPER_RGH_IP, JASPER_RGH_IP]
        metadata = {JASPER_RGH_IP: None, OFFICE_RGH_IP: None}
        for xbox in xboxs:
            print("HI")
