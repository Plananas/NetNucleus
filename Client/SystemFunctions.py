import os
import subprocess
import re

def shutdown():
    #os.system('shutdown -s')
    return "Shutting Down"

def getUpdatableSoftware():
    print("Getting Updatable Software...")
    result = subprocess.run(['winget', 'upgrade'], capture_output=True, text=True)

    # Initialize an empty list to store software update details
    updatableSoftware = []

    # Split the output into lines
    outputLines = result.stdout.splitlines()

    # Skip the first two lines (headers and separators)
    for line in outputLines[2:]:
        # Split each line into parts based on 2 or more spaces
        softwareDetails = re.split(r'\s{2,}', line.strip())

        # Ensure the line has at least 4 parts: Name, ID, Current Version, Available Version
        if len(softwareDetails) >= 4:
            softwareEntry = {
                'name': softwareDetails[0],
                'id': softwareDetails[1],
                'current_version': softwareDetails[2],
                'available_version': softwareDetails[3]
            }
            updatableSoftware.append(softwareEntry)

    return updatableSoftware



