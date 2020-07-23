from pathlib import Path
import argparse
import logging
import os

from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.configure.configure import SymConfig

#function that retrieves the messages from the desired room:
#streamId must be urlsafe
#since=0 is to grab the first message
#limit=100 -> grab 100 messages per loop
#skip=1 -> ensure no duplicate messages are retrieved in get_msg_from_stream()
#returns array of messages
def get_messages(bot_client, streamId, since=0, limit=100, skip=1):
    room_messages = bot_client.get_message_client().get_msg_from_stream(streamId, since, limit=limit, skip=skip)
    return room_messages

#cleans returned messages into format needed for importing:
#streamId -> desired streamId for room importing into (urlSafe)
#returned_messages -> array of messages from get_messages()
#returns array of cleaned message objects ready for import
def clean_messages(returned_messages, streamId):
    import_messages = []
    for i in returned_messages:
        import_message = {"message": "", "data": "", "intendedMessageTimestamp": "", "intendedMessageFromUserId": "", "originatingSystemId": "Symphony", "streamId": str(streamId)}
        import_message.update(message = i.get("message"))
        import_message.update(data = i.get("data"))
        import_message.update(intendedMessageTimestamp = i.get("timestamp"))
        import_message.update(intendedMessageFromUserId = i.get("user").get("userId"))
        import_message.update(originalMessageId = i.get("messageId"))
        import_messages.append(import_message)
    return import_messages

#imports cleaned messages array into desired room:
#cleaned_messages -> array of cleaned message objected returned from clean_messages()
def import_messages(bot_client, cleaned_messages):
    bot_client.get_message_client().import_message(cleaned_messages)
    return None

#called everytime a message is typed to the bot
def run_import(bot_client):
    #initialize import messages functionality when '/import' is typed to bot
    latest_timestamp = 0
    #grab 100 messages at a time and paginate:
    #below is good for < 300 messages: increase accordingly
    for i in range(0,3):
        messages = get_messages(bot_client, "IjYRF9R3zg2Ah2FM51S1mX___o74Bj8CdA", since=latest_timestamp)
        #timestamp of last message fetched above:
        latest_timestamp = messages[0].get("timestamp")
        cleaned_messages = clean_messages(messages, "sUGpQsNXHkKC0-4Ycyk1EX___o72sFO7dA")
        import_messages(bot_client, cleaned_messages)

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--auth", choices=["rsa", "cert"], default="rsa",
            help="Authentication method to use")
        parser.add_argument("--config", help="Config json file to be used")
        args = parser.parse_args()
        # Cert Auth flow: pass path to certificate config.json file
        config_path = args.config
        configure = SymConfig(config_path, config_path)
        configure.load_config()
        if args.auth == "rsa":
            auth = SymBotRSAAuth(configure)
        elif args.auth == "cert":
            auth = Auth(configure)
        else:
            raise ValueError("Unexpected value for auth: " + args.auth)
        auth.authenticate()
        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)
        print('successfully authenticated')
        run_import(bot_client)
        print('successfully imported')


if __name__ == "__main__":
    main()
