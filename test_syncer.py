import os
from syncer import Syncer
from syncer import generate_ftp_instructions
from mongo_client import ConeMongoClient
from helpers import read_json

METADATA_RESPONSE = "b'\r\nZ:\\Private\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo ls -ltra  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nftp> open 192.168.0.233 \r\nConnected to 192.168.0.233.\r\n220 FtpDll Ready\r\n530 Not logged in\r\r\nftp> user xboxftp xboxftp \r\n331 User xboxftp OK, need password\r\n230 User logged in\r\nftp> cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001 \r\n250 Current directory is /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001/\r\nftp> ls -ltra \r\n200 PORT command successful\r\n150 Opening connection\r\n-rwxrwxrwx   1 root root       1093632 Aug 26 2023 Gears2Checkpoint\r\n226 Transfer complete\r\nftp: 72 bytes received in 0.00Seconds 72000.00Kbytes/sec.\r\nftp> quit \r\n221 Goodbye\r\n\r\nZ:\\Private\\dashfox>del retrieve_metadata.txt \r\n'"
METADATA_RESPONSE_FALLOUT_3 = b"\r\nD:\\git\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nD:\\git\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nD:\\git\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/425307D5/00000001  1>>retrieve_metadata.txt \r\n\r\nD:\\git\\dashfox>echo ls -ltra  1>>retrieve_metadata.txt \r\n\r\nD:\\git\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nD:\\git\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nopen 192.168.0.233 \r\nNot logged in\r\r\nuser xboxftp xboxftp \r\ncd /Hdd1/Content/E00000E4D88A136A/425307D5/00000001 \r\nls -ltra \r\n-rwxrwxrwx   1 root root       2465792 Jun 28 2024 Save 24 - Jake  Marigold Station  11..fxs\r\n-rwxrwxrwx   1 root root       2822144 Jun 28 2024 Save 29 - Jake  Craterside Supply  16.fxs\r\n-rwxrwxrwx   1 root root       2859008 Jun 28 2024 Save 30 - Jake  Foggy Bottom Station .fxs\r\n-rwxrwxrwx   1 root root       3162112 Jun 28 2024 Save 32 - Jake  Vault 112  19.39.32.fxs\r\n-rwxrwxrwx   1 root root       3149824 Jun 28 2024 Save 33 - Jake  Vault 112  19.40.45.fxs\r\n-rwxrwxrwx   1 root root       3158016 Jun 28 2024 Save 34 - Jake  Tranquility Lane  19..fxs\r\n-rwxrwxrwx   1 root root       3153920 Jun 28 2024 Save 35 - Jake  Rockwell Residence  1.fxs\r\n-rwxrwxrwx   1 root root       3207168 Jun 28 2024 Save 37 - Jake  Megaton  20.24.35.fxs\r\n-rwxrwxrwx   1 root root       3207168 Jun 28 2024 Save 38 - Jake  Megaton  21.50.47.fxs\r\n-rwxrwxrwx   1 root root       3497984 Jun 28 2024 Save 39 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       3538944 Jun 28 2024 Save 43 - Jake  Upper Deck  25.59.49.fxs\r\n-rwxrwxrwx   1 root root       3624960 Jun 28 2024 Save 46 - Jake  Museum of Technology .fxs\r\n-rwxrwxrwx   1 root root       3620864 Jun 28 2024 Save 47 - Jake  Museum of Technology .fxs\r\n-rwxrwxrwx   1 root root       3624960 Jun 28 2024 Save 48 - Jake  Museum of Technology .fxs\r\n-rwxrwxrwx   1 root root       3624960 Jun 28 2024 Save 49 - Jake  Museum of Technology .fxs\r\n-rwxrwxrwx   1 root root       3674112 Jun 28 2024 Save 51 - Jake  Rivet City  27.11.30.fxs\r\n-rwxrwxrwx   1 root root       3706880 Jun 28 2024 Save 52 - Jake  Megaton  27.12.26.fxs\r\n-rwxrwxrwx   1 root root       8675328 Jan 19 21:17 autosave.fxs\r\n-rwxrwxrwx   1 root root       1478656 Jun 28 2024 Save 2 - Jake  Vault 101 Atrium  01.2.fxs\r\n-rwxrwxrwx   1 root root       1892352 Jun 28 2024 Save 13 - Jake  Big Town  04.25.37.fxs\r\n-rwxrwxrwx   1 root root       3649536 Jun 28 2024 Save 53 - Jake  Stairwell  27.14.03.fxs\r\n-rwxrwxrwx   1 root root       3678208 Jun 28 2024 Save 54 - Jake  RobCo Factory Floor  .fxs\r\n-rwxrwxrwx   1 root root       3657728 Jun 29 2024 Save 55 - Jake  Jefferson Museum and .fxs\r\n-rwxrwxrwx   1 root root       3649536 Jun 29 2024 Save 56 - Jake  Memorial Sub-Basement.fxs\r\n-rwxrwxrwx   1 root root       3641344 Jun 29 2024 Save 57 - Jake  Pump Control  28.11.3.fxs\r\n-rwxrwxrwx   1 root root       4038656 Nov 22 2005 Save 60 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       3809280 Jun 29 2024 Save 59 - Jake  Megaton  28.34.14.fxs\r\n-rwxrwxrwx   1 root root       4149248 Dec 06 23:04 Save 61 - Jake  Evergreen Mills Found.fxs\r\n-rwxrwxrwx   1 root root       4276224 Dec 06 23:45 Save 62 - Jake  Commanding Officer's .fxs\r\n-rwxrwxrwx   1 root root       4308992 Dec 07 00:16 Save 65 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       4759552 Dec 07 15:29 Save 68 - Jake  The Mall  40.50.40.fxs\r\n-rwxrwxrwx   1 root root       4845568 Dec 07 16:22 Save 71 - Jake  Capitol Building West.fxs\r\n-rwxrwxrwx   1 root root       4820992 Dec 07 16:03 Save 70 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       5070848 Dec 07 17:20 Save 74 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       5148672 Dec 07 18:11 Save 75 - Jake  Power Substation  43..fxs\r\n-rwxrwxrwx   1 root root       5324800 Dec 07 18:37 Save 78 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       5566464 Dec 08 11:04 Save 79 - Jake  Robot Repair Center  .fxs\r\n-rwxrwxrwx   1 root root       5517312 Dec 08 11:14 Save 80 - Jake  AntAgonizer's Lair  4.fxs\r\n-rwxrwxrwx   1 root root       5877760 Dec 09 20:59 Save 87 - Jake  Archival Strongroom  .fxs\r\n-rwxrwxrwx   1 root root       5685248 Dec 08 11:43 Save 82 - Jake  Megaton  44.59.16.fxs\r\n-rwxrwxrwx   1 root root       5804032 Dec 08 21:41 Save 84 - Jake  The Capital Wasteland.fxs\r\n-rwxrwxrwx   1 root root       5955584 Dec 09 20:51 Save 86 - Jake  Archival Secure Wing .fxs\r\n-rwxrwxrwx   1 root root       5885952 Dec 09 21:13 Save 88 - Jake  Midship Deck  48.05.4.fxs\r\n-rwxrwxrwx   1 root root       5902336 Dec 09 21:32 Save 89 - Jake  Lamplight Caverns  48.fxs\r\n-rwxrwxrwx   1 root root       6049792 Dec 09 23:52 Save 98 - Jake  Raven Rock - Level 3 .fxs\r\n-rwxrwxrwx   1 root root       5939200 Dec 09 22:14 Save 91 - Jake  Living Quarters  49.0.fxs\r\n-rwxrwxrwx   1 root root       6004736 Dec 09 22:29 Save 93 - Jake  Test Labs  49.21.35.fxs\r\n-rwxrwxrwx   1 root root       6008832 Dec 09 23:30 Save 97 - Jake  Test Labs  50.23.19.fxs\r\n-rwxrwxrwx   1 root root       6037504 Dec 09 23:58 Save 99 - Jake  Raven Rock - Level 2 .fxs\r\n-rwxrwxrwx   1 root root       6066176 Dec 10 00:20 Save 100 - Jake  The Capital Wastelan.fxs\r\n-rwxrwxrwx   1 root root       6098944 Dec 10 00:28 Save 101 - Jake  Citadel - Laboratory.fxs\r\n-rwxrwxrwx   1 root root       6094848 Dec 12 19:51 Save 102 - Jake  Citadel - Laboratory.fxs\r\n-rwxrwxrwx   1 root root       6549504 Dec 12 20:29 Save 103 - Jake  Jefferson Museum and.fxs\r\n-rwxrwxrwx   1 root root       6758400 Dec 12 21:20 Save 104 - Jake  Satellite Facility  .fxs\r\n-rwxrwxrwx   1 root root       6762496 Dec 12 21:28 Save 105 - Jake  Citadel - A Ring  52.fxs\r\n-rwxrwxrwx   1 root root       6909952 Dec 13 18:23 Save 108 - Jake  Outcast Outpost  53..fxs\r\n-rwxrwxrwx   1 root root       6897664 Dec 12 22:10 Save 107 - Jake  Megaton  53.06.29.fxs\r\n-rwxrwxrwx   1 root root       6909952 Dec 13 18:23 Save 109 - Jake  Outcast Outpost  53..fxs\r\n-rwxrwxrwx   1 root root       6991872 Dec 13 22:14 Save 110 - Jake  Command Tent  55.15..fxs\r\n-rwxrwxrwx   1 root root       7143424 Dec 13 23:18 Save 111 - Jake  Anchorage  55.31.10.fxs\r\n-rwxrwxrwx   1 root root       7122944 Dec 14 20:32 Save 112 - Jake  Anchorage  55.34.20.fxs\r\n-rwxrwxrwx   1 root root       7139328 Dec 14 20:34 Save 113 - Jake  Anchorage  55.36.12.fxs\r\n-rwxrwxrwx   1 root root       7348224 Dec 15 20:57 Save 118 - Jake  Anchorage  56.05.26.fxs\r\n-rwxrwxrwx   1 root root       7159808 Dec 14 20:38 Save 115 - Jake  Anchorage  55.40.37.fxs\r\n-rwxrwxrwx   1 root root       7282688 Dec 14 20:54 Save 117 - Jake  Anchorage  55.56.49.fxs\r\n-rwxrwxrwx   1 root root       7331840 Dec 15 21:30 Save 121 - Jake  Anchorage  56.37.49.fxs\r\n-rwxrwxrwx   1 root root       7368704 Dec 15 21:43 Save 122 - Jake  Outcast Outpost  56..fxs\r\n-rwxrwxrwx   1 root root       7688192 Dec 21 23:21 Save 125 - Jake  Point Lookout  58.24.fxs\r\n-rwxrwxrwx   1 root root       8245248 Dec 22 01:15 Save 126 - Jake  Lighthouse  60.19.12.fxs\r\n-rwxrwxrwx   1 root root       8310784 Dec 23 11:13 Save 129 - Jake  Sacred Bog  60.42.48.fxs\r\n-rwxrwxrwx   1 root root       8310784 Dec 22 01:38 Save 128 - Jake  Sacred Bog  60.41.34.fxs\r\n-rwxrwxrwx   1 root root       8396800 Dec 23 12:53 Save 134 - Jake  Point Lookout  62.19.fxs\r\n-rwxrwxrwx   1 root root       8396800 Dec 23 12:34 Save 133 - Jake  Point Lookout  61.59.fxs\r\n-rwxrwxrwx   1 root root       8466432 Dec 23 21:17 Save 137 - Jake  The Capital Wastelan.fxs\r\n-rwxrwxrwx   1 root root       8441856 Dec 23 14:08 Save 136 - Jake  Point Lookout  63.33.fxs\r\n-rwxrwxrwx   1 root root       8515584 Dec 23 21:20 Save 138 - Jake  The Capital Wastelan.fxs\r\n-rwxrwxrwx   1 root root       8544256 Dec 29 00:44 Save 139 - Jake  The Capital Wastelan.fxs\r\n-rwxrwxrwx   1 root root       8495104 Dec 29 19:24 Save 142 - Jake  Rivet City  65.51.59.fxs\r\n-rwxrwxrwx   1 root root       8474624 Dec 29 18:57 Save 141 - Jake  Megaton  65.25.12.fxs\r\n-rwxrwxrwx   1 root root       8646656 Dec 30 20:37 Save 145 - Jake  Megaton  67.40.56.fxs\r\n-rwxrwxrwx   1 root root       8613888 Dec 30 20:08 Save 144 - Jake  Arlington National C.fxs\r\n-rwxrwxrwx   1 root root       8642560 Jan 19 19:55 Save 146 - Jake  The Capital Wastelan.fxs\r\n-rwxrwxrwx   1 root root       8679424 Jan 19 23:42 Save 147 - Jake  Old Olney Undergroun.fxs\r\nquit \r\n\r\nD:\\git\\dashfox>del retrieve_metadata.txt \r\n"


def test_get_max_last_modified():
    syncer = Syncer()
    # ftp_dump = syncer.query_all()
    # print("HERE IS THE FTP DUMP:")
    # print(ftp_dump)
    coneMongo = ConeMongoClient()
    mock_syncer_response = read_json("xbox_syncer_response.json")
    # coneMongo.insert_ftp_dump(mock_syncer_response)
    results = coneMongo.get_all_ftp_dump()
    print(len(results))
    latest_ftp_dump = coneMongo.get_lastest_ftp_dump()
    print("LATEST")
    print(latest_ftp_dump)
    generate_ftp_instructions(latest_ftp_dump)


test_get_max_last_modified()
