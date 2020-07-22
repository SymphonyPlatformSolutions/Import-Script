# Import-Script
Python Script for importing messages from one room into another


# Usage: 

$ python3 main_import.py --auth "rsa" --config "path/to/config.json"

This import script leverages the Import Message API endpoint: https://developers.symphony.com/restapi/reference#import-message-v4 allowing bots to import messages into Symphony from another system or from one chatroom to another.  Messages will retain their original sender, timestamp and be imported in the order to which they were sent.  This endpoint takes a list of messages as input.  If an import fails on a given message, the rest of the operation will continue.

This specific script is designed to import messages from one chatroom in Symphony to another in Symphony.  When the bot starts, it grabs the first 100 messages, cleans them, and import them.  It repeats this process for the next batch of 100 messages, updating the latest timestamp on each iteration to avoid importing any duplicate messages.  This process repeats until all of the messages are obtained, cleaned, and imported.

Note: The origin streamID, destination streamID, number of messages obtained in a batch, as well as the earliest message you wish to retrieve are all configurable by editing the script directly.  

For private rooms, bots must be in the room in order to access messages or import messages.  


