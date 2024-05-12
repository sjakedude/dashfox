import os
from syncer import Syncer


METADATA_RESPONSE_SINGLE_SAVE = "b'\r\nZ:\\Private\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo ls  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nopen 192.168.0.233 \r\nNot logged in\r\r\nuser xboxftp xboxftp \r\ncd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001 \r\nls \r\n-rwxrwxrwx   1 root root       1093632 Aug 26 2023 Gears2Checkpoint\r\nquit \r\n\r\nZ:\\Private\\dashfox>del retrieve_metadata.txt \r\n'"
METADATA_RESPONSE_MULTIPLE_SAVE = "b'\r\nZ:\\Private\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo ls  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nopen 192.168.0.233 \r\nNot logged in\r\r\nuser xboxftp xboxftp \r\ncd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001 \r\nls \r\n-rwxrwxrwx   1 root root       1093632 Aug 26 2023 Gears2Checkpoint\r\nquit \r\n\r\nZ:\\Private\\dashfox>del retrieve_metadata.txt \r\n'"


def test_get_last_modified():
    syncer = Syncer("xbox_360")
    res = syncer.get_last_modified(METADATA_RESPONSE, "Gears2Checkpoint")
    print(res)

test_get_last_modified()
