import os
from syncer import Syncer


METADATA_RESPONSE = "b'\r\nZ:\\Private\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo date -r . +%s  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nopen 192.168.0.233 \r\nNot logged in\r\r\nuser xboxftp xboxftp \r\ncd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001 \r\ndate -r . +%s \r\n1719255989\r\nquit \r\n\r\nZ:\\Private\\dashfox>del retrieve_metadata.txt \r\n'"


def test_get_last_modified():
    syncer = Syncer("sjakedude", "gears_of_war_2")
    res = syncer.get_last_modified(METADATA_RESPONSE)
    print(res)

test_get_last_modified()
