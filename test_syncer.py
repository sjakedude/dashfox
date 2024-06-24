import os
from syncer import Syncer


METADATA_RESPONSE = "b'\r\nZ:\\Private\\dashfox>echo open 192.168.0.233  1>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo user xboxftp xboxftp  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo ls -ltra  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>echo quit  1>>retrieve_metadata.txt \r\n\r\nZ:\\Private\\dashfox>ftp -n -s:retrieve_metadata.txt \r\nftp> open 192.168.0.233 \r\nConnected to 192.168.0.233.\r\n220 FtpDll Ready\r\n530 Not logged in\r\r\nftp> user xboxftp xboxftp \r\n331 User xboxftp OK, need password\r\n230 User logged in\r\nftp> cd /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001 \r\n250 Current directory is /Hdd1/Content/E00000E4D88A136A/4D53082D/00000001/\r\nftp> ls -ltra \r\n200 PORT command successful\r\n150 Opening connection\r\n-rwxrwxrwx   1 root root       1093632 Aug 26 2023 Gears2Checkpoint\r\n226 Transfer complete\r\nftp: 72 bytes received in 0.00Seconds 72000.00Kbytes/sec.\r\nftp> quit \r\n221 Goodbye\r\n\r\nZ:\\Private\\dashfox>del retrieve_metadata.txt \r\n'"


def test_get_last_modified():
    syncer = Syncer("sjakedude", "gears_of_war_2")
    res = syncer.get_last_modified(METADATA_RESPONSE)
    print(res)

test_get_last_modified()
