import os
from syncer import Syncer
from syncer import generate_ftp_instructions
from mongo_client import ConeMongoClient
from helpers import read_json
import json


def test_get_max_last_modified():
    syncer = Syncer()
    ftp_dump = syncer.query_all()
    print("HERE IS THE FTP DUMP:")
    print(json.dumps(ftp_dump))
    # coneMongo = ConeMongoClient()
    # mock_syncer_response = read_json("xbox_syncer_response.json")
    # coneMongo.insert_ftp_dump(mock_syncer_response)
    # results = coneMongo.get_all_ftp_dump()
    # print(len(results))
    # latest_ftp_dump = coneMongo.get_lastest_ftp_dump()
    # print("LATEST")
    # print(latest_ftp_dump)
    ftp_instructions = generate_ftp_instructions(ftp_dump)
    print("====")
    print(ftp_instructions)


test_get_max_last_modified()
