# This is the python script that connects to all available RGH xbox 360 consooles
# and checks every save file metadata for when it was last modified and syncs the
# save files to the other consoles so they are all up to date with the latest save

import json
import re
from subprocess import check_output
from datetime import datetime
import time
from helpers import read_json
from helpers import get_month_from_string

ENV = "prod"


class Syncer:

    def __init__(self):
        self.config = read_json("xbox_config.json")
        self.profiles = ["E00000E4D88A136A", "E8687BFFA45BBA40"]
        self.xboxs = ["192.168.0.233", "192.168.0.215"]
        self.games = [
            "425307D5",
            "4D53082D",
            "415607E6",
            "41560817",
            "4156081C",
            "41560855",
            "425307E3",
            "425307E6",
            "454108E6",
            "45410998",
            "4B4D07DF",
            "4B4D07F2",
            "4C4107D1",
            "4D5307F1",
            "4D53085B",
            "4D5308AB",
            "4D530910",
            "5454082B",
            "584111F7",
            "5841128F",
        ]

    def purge_old_saves(self):
        check_output(
            f"Z:\Private\conecommons\scripts\\rom_sync\\purge_old_saves.bat",
            shell=True,
        )
        print("Old saves deleted from NAS")

    def download_save_file(self, xbox, profile, title_id, save):

        print(f"Downloading {save} from {xbox}")
        check_output(
            f'Z:\Private\conecommons\scripts\\rom_sync\\download_xbox_file.bat {xbox} {profile} {title_id} "{save}"',
            shell=True,
        )
        print(f"Latest save file {save} downloaded from {xbox}")

    def upload_save_file(self, xbox, profile, title_id, save):
        print(f"About to upload {profile}/{title_id}/{save} files to {xbox}")
        check_output(
            f'Z:\Private\conecommons\scripts\\rom_sync\\upload_xbox_file.bat {xbox} {profile} {title_id} "{save}"',
            shell=True,
        )
        print(f"Latest save file {save} uploaded to {xbox}")

    def download_title_id_directory(self, xbox, profile, title_id):

        print(f"Downloading {profile}/{title_id} from {xbox}")
        check_output(
            f"Z:\Private\conecommons\scripts\\rom_sync\\download_xbox_title_id.bat {xbox} {profile} {title_id}",
            shell=True,
        )
        print(f"{profile}/{title_id} downloaded from {xbox}")

    def create_directories_on_nas(self):
        for profile in self.profiles:
            for title_id in self.games:
                print(f"Creating {profile}/{title_id}/00000001 on NAS")
                check_output(
                    f"Z:\Private\conecommons\scripts\\rom_sync\\create_directory_on_nas.bat {profile} {title_id}",
                    shell=True,
                )
                print(f"Created {profile}/{title_id}/00000001 on NAS")

    def create_directory_on_xbox(self, xbox, profile, title_id):
        print(f"Creating {profile}/{title_id}/00000001 on {xbox}")
        check_output(
            f"Z:\Private\conecommons\scripts\\rom_sync\\create_directory_on_xbox.bat {xbox} {profile} {title_id}",
            shell=True,
        )
        print(f"Created {profile}/{title_id}/00000001 on {xbox}")

    def download_profile_directory(self, xbox, profile):

        self.create_directory_on_nas(profile)
        print(f"Downloading {profile} from {xbox}")
        check_output(
            f"Z:\Private\conecommons\scripts\\rom_sync\\download_xbox_profile.bat {xbox} {profile}",
            shell=True,
        )
        print(f"{profile} downloaded from {xbox}")

    def query_all(self):
        master = {}

        # Connect to each xbox and retrieve metadata for each profile and each game within that profile
        for xbox in self.xboxs:
            master[xbox] = {}
            for profile in self.profiles:
                master[xbox][profile] = {}
                for game in self.games:
                    output = None
                    if ENV == "local":
                        output = str(
                            check_output(
                                f"D:\\git\\conecommons\\scripts\\rom_sync\\retrieve_xbox_metadata.bat {xbox} {profile} {game}",
                                shell=True,
                            )
                        )
                    else:
                        output = str(
                            check_output(
                                f"Z:\Private\conecommons\scripts\\rom_sync\\retrieve_xbox_metadata.bat {xbox} {profile} {game}",
                                shell=True,
                            )
                        )
                    files_dict = parse_filenames_and_dates(output)
                    if files_dict != {}:
                        master[xbox][profile][game] = files_dict
                if master[xbox][profile] == {}:
                    del master[xbox][profile]
        return master


def parse_filenames_and_dates(output):
    files = {}
    trimmed_output = output.split("Opening connection")[1]
    trimmed_output = trimmed_output.split("Transfer complete")[0]
    for token in trimmed_output.split("-rwxrwxrwx"):
        line = token.split()
        if line[0] == "1" and line[1] == "root" and line[2] == "root":
            # its a file
            size = line[3]
            month = line[4]
            day = line[5]
            year = line[6]
            time = line[6]
            if ":" in year:
                year = datetime.now().year
            if ":" not in time:
                time = "00:00"
            date_obj = datetime(
                int(year),
                get_month_from_string(month),
                int(day),
                int(time.split(":")[0]),
                int(time.split(":")[0]),
                0,
            )
            last_modified_epoch = int(date_obj.timestamp())
            filename = token.split(f"{month} {day} {line[6]} ")[1]
            filename = filename.replace("\\r\\n", "")
            files[filename] = {
                "last_modified": f"{month} {day} {year} {time}",
                "last_modified_epoch": last_modified_epoch,
                "size": size,
            }
    return files


def generate_ftp_instructions(ftp_dump):
    instructions = []
    latest_map = {}
    if ftp_dump.get("_id"):
        del ftp_dump["_id"]
    if len(ftp_dump.keys()) > 1:
        # More than 1 xbox ip was pulled in from FTP
        for xbox_ip in ftp_dump.keys():
            # For each xbox ip, check if the other keys have each title_id present
            print(f"Currently on {xbox_ip}")
            for profile in ftp_dump[xbox_ip].keys():
                latest_map[profile] = {}
                print(f"Currently on {xbox_ip} in {profile}")
                for other_xbox_ip in ftp_dump.keys():
                    if other_xbox_ip != xbox_ip:
                        if ftp_dump[other_xbox_ip].get(profile):
                            print(
                                f"Both {xbox_ip} and {other_xbox_ip} have profile {profile}"
                            )
                            for title_id in ftp_dump[xbox_ip][profile].keys():
                                latest_map[profile][title_id] = {}
                                if ftp_dump[other_xbox_ip][profile].get(title_id):
                                    print(
                                        f"Both {xbox_ip} and {other_xbox_ip} have profile {profile} and title_id {title_id}"
                                    )
                                    for save_file in ftp_dump[xbox_ip][profile][
                                        title_id
                                    ].keys():
                                        if (
                                            save_file
                                            not in latest_map[profile][title_id].keys()
                                        ):
                                            latest_map[profile][title_id][save_file] = (
                                                ftp_dump[other_xbox_ip][profile][
                                                    title_id
                                                ]["last_modified_epoch"],
                                                xbox_ip,
                                            )

                                        if ftp_dump[other_xbox_ip][profile][
                                            title_id
                                        ].get(save_file):
                                            print(
                                                f"Both {xbox_ip} and {other_xbox_ip} have profile {profile} and title_id {title_id} and game save {save_file}. Now picking the latest version."
                                            )
                                            if (
                                                ftp_dump[other_xbox_ip][profile][
                                                    title_id
                                                ][save_file]["last_modified_epoch"]
                                                > latest_map[profile][title_id][
                                                    save_file
                                                ][0]
                                            ):
                                                latest_map[profile][title_id][
                                                    save_file
                                                ] = (
                                                    ftp_dump[other_xbox_ip][profile][
                                                        title_id
                                                    ][save_file]["last_modified_epoch"],
                                                    other_xbox_ip,
                                                )
                                        else:
                                            print(
                                                f"{other_xbox_ip} does not have gamesave {save_file} under title_id {title_id} under profile {profile}"
                                            )
                                            instructions.append(
                                                {
                                                    "source_ip": xbox_ip,
                                                    "destination_ip": other_xbox_ip,
                                                    "path": f"{profile}/{title_id}/{save_file}",
                                                }
                                            )
                                else:
                                    print(
                                        f"{other_xbox_ip} does not have title_id {title_id} under profile {profile}"
                                    )
                                    for save_file in ftp_dump[xbox_ip][profile][
                                        title_id
                                    ]:
                                        instructions.append(
                                            {
                                                "source_ip": xbox_ip,
                                                "destination_ip": other_xbox_ip,
                                                "path": f"{profile}/{title_id}/{save_file}",
                                            }
                                        )
                        else:
                            print(f"{other_xbox_ip} does not have profile {profile}")
                            for title_id in ftp_dump[xbox_ip][profile]:
                                for save_file in ftp_dump[xbox_ip][profile][title_id]:
                                    instructions.append(
                                        {
                                            "source_ip": xbox_ip,
                                            "destination_ip": other_xbox_ip,
                                            "path": f"{profile}/{title_id}/{save_file}",
                                        }
                                    )
        for profile in latest_map.keys():
            for title_id in latest_map[profile].keys():
                for save_file in latest_map[profile][title_id].keys():
                    for xbox_ip in ftp_dump.keys():
                        if xbox_ip != save_file[1]:
                            print(
                                f"{xbox_ip} does not have the latest version of {save_file}"
                            )
                            instructions.append(
                                {
                                    "source_ip": save_file[1],
                                    "destination_ip": xbox_ip,
                                    "path": f"{profile}/{title_id}/{save_file}",
                                }
                            )
    return instructions


def handle_ftp_instructions(syncer, instructions):
    for ftp_instruction in instructions:
        path_parts = ftp_instruction["path"].split("/")
        profile = path_parts[0]
        title_id = path_parts[1]
        file_name = path_parts[2]
        syncer.download_save_file(
            ftp_instruction["source_ip"], profile, title_id, file_name
        )
        syncer.create_directory_on_xbox(ftp_instruction["destination_ip"], profile, title_id)
        syncer.upload_save_file(ftp_instruction["destination_ip"], profile, title_id, file_name)