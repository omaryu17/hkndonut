import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
client = WebClient(token=BOT_TOKEN)


def get_members():
    metadata = client.users_list()
    members = metadata["members"]
    member_info = []
    for info in members:
        if not info["is_bot"] and not (info["id"] == "USLACKBOT"):
            member_info.append((info["name"], info["id"], info["profile"]["email"]))
    return member_info


def assign_pairs():
    return None

members = get_members()
my_id = members[0][1]

try:
    message = "monkfish"

    # prefix = ()

    # message += prefix

    # # for mapping in assignments:
    # #     info = f'<@{mapping}> please help <{assignments[mapping][1]}|@{assignments[mapping][0]}> \n'
    # #     message += info

    #response = client.chat_postMessage(channel="general", text=message)

    # SENDING DIRECTS
    convo = client.conversations_open(users=[my_id])
    dm = convo["channel"]["id"]
    response = client.chat_postMessage(channel=dm, text=message)

except SlackApiError as e:
    assert e.response["error"]