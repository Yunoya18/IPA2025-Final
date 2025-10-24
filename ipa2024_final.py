#######################################################################################
# Yourname: Sonrasamon Meepasee
# Your student ID: 66070200
# Your GitHub Repo: https://github.com/Yunoya18/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import time
import os
import requests
import json
from dotenv import load_dotenv
from requests_toolbelt import MultipartEncoder
import restconf_final
import netconf_final
import netmiko_final
import ansible_final

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm"
)

method = ""

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer " + ACCESS_TOKEN}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070200"):

        # extract the command
        all_command = message.split()
        command = all_command[1].strip()
        print(command)

        if len(all_command) < 3:
            if command in ['restconf', 'netconf']:
                responseMessage = f"Ok: {command.capitalize()}"
                method = command
            elif command in ['gigabit_status', 'showrun']:
                if command == "gigabit_status":
                    responseMessage = netmiko_final.gigabit_status()
                elif command == "showrun":
                    responseMessage = ansible_final.showrun()
            else:
                if method == "":
                    responseMessage = "Error: No method specified"
                else:
                    if command in ['create', 'delete', 'enable', 'disable', 'status', 'gigabit_status', 'showrun', 'motd']:
                        responseMessage = "Error: No IP specified"
                    else:
                        responseMessage = "Error: No command found."
        elif len(all_command) == 3:
            ip = all_command[1].strip()
            command = all_command[2].strip()
            if command == "gigabit_status":
                responseMessage = netmiko_final.gigabit_status(ip)
            elif command == "showrun":
                responseMessage = ansible_final.showrun(ip)
            elif command == "motd":
                responseMessage = netmiko_final.get_motd(ip)
            else:
                if method == "restconf":
                    if command == "create":
                        responseMessage = restconf_final.create(ip)
                    elif command == "delete":
                        responseMessage = restconf_final.delete(ip)
                    elif command == "enable":
                        responseMessage = restconf_final.enable(ip)
                    elif command == "disable":
                        responseMessage = restconf_final.disable(ip)
                    elif command == "status":
                        responseMessage = restconf_final.status(ip)
                    else:
                        responseMessage = "Error: No command or unknown command"
                elif method == "netconf":
                    if command == "create":
                        responseMessage = netconf_final.create(ip)
                    elif command == "delete":
                        responseMessage = netconf_final.delete(ip)
                    elif command == "enable":
                        responseMessage = netconf_final.enable(ip)
                    elif command == "disable":
                        responseMessage = netconf_final.disable(ip)
                    elif command == "status":
                        responseMessage = netconf_final.status(ip)
                    else:
                        responseMessage = "Error: No command or unknown command"
                else:
                    responseMessage = "Error: No method specified"
        elif len(all_command) > 3:
            ip = all_command[1].strip()
            command = all_command[2].strip()
            txt = " ".join(all_command[3:])
            if command == "motd":
                responseMessage = ansible_final.set_motd(ip, txt)
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            filename = "show_run_66070200_Router.txt"
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            postData = {
                "roomId": roomIdToGetMessages,
                "text": "show running config",
                "files": (filename, fileobject, filetype)
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
                "Authorization": 'Bearer ' + ACCESS_TOKEN,
                "Content-Type": postData.content_type,
            }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": 'Bearer ' + ACCESS_TOKEN, "Content-Type": "application/json"}

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
