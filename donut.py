import os
import json
import copy
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# load environment variables and authenticate bot
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
client = WebClient(token=BOT_TOKEN)


# read list of members
def read_members():
    file = open("members.json", "r")
    try:
        data = json.load(file)
    except json.decoder.JSONDecodeError as e:
        data = None
    file.close()
    return data


# write list of members
def write_members(members: list):
    file = open("members.json", "w")
    json.dump(members, file)
    file.close()


# read hashmap of matchings availabilities
def read_matchings():
    file = open("matchings.json", "r")
    try:
        data = json.load(file)
    except json.decoder.JSONDecodeError as e:
        data = None
    file.close()
    return data


# write hashmap of matchings availabilities
def write_matchings(matchings: dict):
    file = open("matchings.json", "w")
    json.dump(matchings, file)
    file.close()


# write list of pairs
def write_pairs(pairs: list):
    file = open("pairs.txt", "w")
    json.dump(pairs, file)
    file.close()


# get list of member infos in channel
def get_members():
    metadata = client.users_list()
    members = metadata["members"]
    member_info = [] #{}
    for info in members:
        if not info["is_bot"] and not (info["id"] == "USLACKBOT"):
            member_info.append((info["name"], info["id"])) #, info["profile"]["email"]
    return member_info


# populate matchings with initial data
def populate_matchings(members: list):
    matchings = {}
    for member in members:
        id = member[1]
        for other in members:
            if member is not other:
                if id not in matchings:
                    matchings[id] = []
                    matchings[id].append(other)
                else:
                    matchings[id].append(other)
    
    return matchings


# add new user to data
def add_new(channel_members, file_members, matchings):
    # TODO handle multiple new users 
    new_member = None
    for member in channel_members:
        if member not in file_members:
            new_member = copy.deepcopy(member)
            break
    
    file_members.append(new_member)
    
    matchings[new_member["id"]] = []


# assign donut pairs and update matchings
def assign_pairs(matchings: dict):
    return []


# send DMs to pairs
def dm_pairs(pairs: list):
    try:
        message = "donut"

        # prefix = ()

        # message += prefix

        # # for mapping in assignments:
        # #     info = f'<@{mapping}> please help <{assignments[mapping][1]}|@{assignments[mapping][0]}> \n'
        # #     message += info

        #response = client.chat_postMessage(channel="general", text=message)

        # SENDING DIRECTS
        convo = client.conversations_open(users=["U048F048TDF", "U059TLPBXK5"])
        dm = convo["channel"]["id"]
        response = client.chat_postMessage(channel=dm, text=message)

    except SlackApiError as e:
        assert e.response["error"]


# driver function
def main():
    # get channel member infos
    channel_members = get_members()

    file_members = read_members()
    matchings = read_matchings()

    if file_members == None:
        file_members = copy.deepcopy(channel_members)

    if matchings == None:
        matchings = populate_matchings(channel_members)
    
    if len(channel_members) != len(file_members):
        # TODO handle multiple new users
        add_new(channel_members, file_members, matchings)

    pairs = assign_pairs(matchings)

    write_pairs(pairs)

    write_members(file_members)

    write_matchings(matchings)

    dm_pairs()


if __name__ == "__main__":
    main()