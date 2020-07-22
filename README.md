# Import-Script
Python Script for importing messages from one room into another


# Usage: 

$ python3 main_import.py --auth "rsa" --config "path/to/config.json"

This import script leverages the Import Message API endpoint: https://developers.symphony.com/restapi/reference#import-message-v4 allowing bots to import messages into Symphony from another system or from one chatroom to another.  Messages will retain their original sender, timestamp and be imported in the order to which they were sent.  This endpoint takes a list of messages as input.  If an import fails on a given message, the rest of the operation will continue.


