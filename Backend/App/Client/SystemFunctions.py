import os
import subprocess
import re
import json

def shutdown():
    #os.system('shutdown -s')
    return "Shutting Down"

#TODO change the methods in this function to all use chocolatey
def get_updatable_software():
    print("Getting Updatable Software...")

    # Run the choco upgrade command to get the list of outdated packages
    result = subprocess.run(['choco', 'upgrade', '--all', '--output', 'json'], capture_output=True, text=True)

    # Initialize an empty list to store software update details
    updatableSoftware = []

    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return updatableSoftware

    # The output is expected to be in JSON format
    try:
        # Parse the output as JSON
        output = json.loads(result.stdout)

        for software in output:
            # Only include software that is actually upgradable
            if 'package' in software and 'versions' in software:
                softwareEntry = {
                    'name': software['package'],
                    'id': software['package'],
                    'current_version': software['versions']['installed'],
                    'available_version': software['versions']['available']
                }
                updatableSoftware.append(softwareEntry)
    except json.JSONDecodeError:
        print("Failed to decode the JSON output from Chocolatey.")

    return updatableSoftware

#TODO test
def get_all_software():
    print("Getting all installed software...")
    try:
        result = subprocess.run(['choco', 'list'], capture_output=True, text=True, encoding='utf-8')
    except Exception as e:
        # Catch any other exceptions that might occur
        print(f"An unexpected error occurred: {str(e)}")
        return []
    # Check if the command was successful
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        print(f"Exit code: {result.returncode}")
        return []

    # Print the stdout for debugging
    print("Command Output:")
    print(result.stdout)

    print("got all the software")
    installedSoftware = []
    outputLines = result.stdout.splitlines()

    for line in outputLines:
        if not line or '---' in line:
            continue

        softwareDetails = re.split(' ', line.strip())  # 2 or more spaces

        # In case the line has 2 parts (Package, Version)
        if len(softwareDetails) == 2:
            name, version = softwareDetails
            softwareEntry = {
                'name': name,
                'version': version,
            }
            installedSoftware.append(softwareEntry)

    return installedSoftware


#TODO change to chocolatey
def install_program(program_name):
    try:
        # Run the winget command to install the program
        subprocess.run(['winget', 'install', program_name], check=True)
        return f"Successfully installed {program_name}"
    except subprocess.CalledProcessError:
        return f"Failed to install {program_name}"
    except FileNotFoundError:
        return "winget is not installed or available on this system."

#TODO change to chocolatey
def uninstall_program(program_name):
    try:
        # List installed instances of the program
        result = subprocess.run(
            ['choco', 'uninstall' , '--id', program_name],
            capture_output=True, text=True, check=True
        )
        output = result.stdout

        # Extract IDs from the output using fixed-width parsing
        lines = output.splitlines()
        ids = []

        if not ids:
            return f"No instances of {program_name} found to uninstall."

        # Uninstall each instance by ID
        for program_id in ids:
            subprocess.run(['winget', 'uninstall', '--id', program_id, '--silent'], check=True)

        return f"Successfully uninstalled all instances of {program_name}."

    except subprocess.CalledProcessError as e:
        return f"Failed to uninstall {program_name}. Error: {e}"
    except FileNotFoundError:
        return "winget is not installed or available on this system."
