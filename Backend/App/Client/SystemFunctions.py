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
        softwareDetails = re.split(r'\s{3,}', line.strip())

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

def getAllSoftware():
    print("Getting all installed software...")
    result = subprocess.run(['winget', 'list'], capture_output=True, text=True, encoding='utf-8')

    # Initialize an empty list to store software details
    installedSoftware = []

    # Split the output into lines
    outputLines = result.stdout.splitlines()

    # Skip the first 2 lines (headers and separators) and start from the actual data
    for line in outputLines:
        # Split each line into parts based on 2 or more spaces
        softwareDetails = re.split(r'\s{2,}|…', line.strip())

        # Handle cases where the line may have only 2 parts (e.g., missing version)
        if len(softwareDetails) < 3:
            # Add the software entry to the list
            continue

        # Handle cases where the version is listed as "winget"
        if softwareDetails[2].lower() == "winget":
            version = "N/A"

        # Add the software entry to the list
        softwareEntry = {
            'name': softwareDetails[0],
            'id': softwareDetails[1],
            'version': softwareDetails[2],
        }
        installedSoftware.append(softwareEntry)

    return installedSoftware

def install_program(program_name):
    try:
        # Run the winget command to install the program
        subprocess.run(['winget', 'install', program_name], check=True)
        print(f"Successfully installed {program_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {program_name}")
    except FileNotFoundError:
        print("winget is not installed or available on this system.")

def uninstall_program(program_name):
    try:
        subprocess.run(['winget', 'uninstall', program_name], check=True)
        print(f"Successfully uninstalled {program_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to uninstall {program_name}")
    except FileNotFoundError:
        print("winget is not installed or available on this system.")
