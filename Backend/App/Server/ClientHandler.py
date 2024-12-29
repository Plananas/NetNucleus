import uuid
import ast

from Backend.App.Models.ClientModel import ClientModel
from Backend.App.Models.MessageController import MessageController
from Backend.App.Models.ProgramModel import ProgramModel
from Backend.App.Repositories.ClientRepository import ClientRepository
from Backend.App.Repositories.ProgramRepository import ProgramRepository


class ClientHandler:

    SHUTDOWN_COMMAND = "shutdown"
    GET_UPGRADES_COMMAND = "upgrades"
    GET_ALL_SOFTWARE_COMMAND = "software"
    INSTALL_SOFTWARE_COMMAND = "install"
    UNINSTALL_SOFTWARE_COMMAND = "uninstall"

    SUCCESSFUL_UNINSTALL_MESSAGE = "Successfully uninstalled"
    SUCCESSFUL_INSTALL_MESSAGE = "Successfully installed"

    def __init__(self, message_controller):
        self.messageController: MessageController = message_controller
        self.connectedStatus = False
        self.clientModel = self.get_client_with_software()
        self.get_available_updates()

    def shutdown(self):
        self.messageController.write(self.SHUTDOWN_COMMAND)

        #the client is shutting down so I think putting some kind of behaviour to check the status would be good
        response = self.messageController.read()
        return response

    def get_available_updates(self):
        """
        :return: Array of Software available to update
        """
        self.messageController.write(self.GET_UPGRADES_COMMAND)

        responseArray = self.messageController.read()
        responseArray = ast.literal_eval(responseArray)

        mac, programs = next(iter(responseArray.items()))
        for program in programs:
            print(program)
            self.save_program(self.clientModel.get_uuid() ,program)

        return responseArray


    def get_client_with_software(self) -> ClientModel :
        """
        :return: Array of Software
        """
        self.messageController.write(self.GET_ALL_SOFTWARE_COMMAND)

        responseArray = self.messageController.read()
        print("RESPONSE ARRAY")
        print(responseArray)
        responseArray = ast.literal_eval(responseArray)
        client = self.save_client(responseArray)

        return client


    def installSoftware(self, software_name):
        """
        :return: Success Message
        """
        self.messageController.write((self.INSTALL_SOFTWARE_COMMAND + " " + software_name))

        responseArray = self.messageController.read()
        responseArray = ast.literal_eval(responseArray)  # Assuming it's a string representation of a list
        mac_address = self.clientModel.get_mac_address()

        response = responseArray[mac_address]
        print(response)

        # Check if "Successful" is in the response
        if self.SUCCESSFUL_INSTALL_MESSAGE in response:
            print("Uninstallation was successful.")
            self.get_client_with_software()
        else:
            print("Uninstallation failed or status unknown.")

        return responseArray

    def uninstall_software(self, software_name):
        """
        :return: Success Message
        """
        self.messageController.write((self.UNINSTALL_SOFTWARE_COMMAND + " " + software_name))

        responseArray = self.messageController.read()
        responseArray = ast.literal_eval(responseArray)  # Assuming it's a string representation of a list
        mac_address = self.clientModel.get_mac_address()

        response = responseArray[mac_address]
        print(response)

        # Check if "Successful" is in the response
        if self.SUCCESSFUL_UNINSTALL_MESSAGE in response:
            print("Uninstallation was successful.")
            self.get_client_with_software()
        else:
            print("Uninstallation failed or status unknown.")

        return responseArray


    def save_client(self, mac_and_software) -> ClientModel:
        mac_address = next(iter(mac_and_software))
        client_repository = ClientRepository()
        existing_client = client_repository.get_client_by_mac_address(mac_address)

        if existing_client:
            client_uuid = existing_client[0].get_uuid()  # Assuming the existing client has a 'uuid' field
            print('Client exists')
            existing_client[0].set_shutdown(False)
        else:
            client_uuid = str(uuid.uuid4())
            print('Client does not exist: Creating Model')

            self.clientModel: ClientModel = ClientModel(
                uuid=client_uuid,
                mac_address=mac_address,
                nickname='',
                shutdown=False,
                updatable_programs=''
            )
            self.clientModel.save()
            existing_client = [self.clientModel]

        # Save the associated program
        self.save_programs(client_uuid, mac_and_software[mac_address])

        return existing_client[0]

    def save_programs(self, client_uuid, installed_software):
        #TODO delete existing software and replace with the current ones
        program_repository = ProgramRepository()
        existing_program = program_repository.get_program_by_client_id(client_uuid)
        if existing_program:
            for program in existing_program:
            #The program should already exist if it had a version so we delete it
                program.delete()

        for program in installed_software:
            self.save_program(client_uuid, program)

    def save_program(self, client_uuid, program):
        program_repository = ProgramRepository()
        print(program)
        existing_program = program_repository.get_program_by_client_id_and_name(client_uuid, program["name"])

        if existing_program:
            #The program should already exist if it had a version so we delete it
            existing_program[0].delete()

        programModel = ProgramModel(
            client_uuid=client_uuid,
            name=program["name"],
            current_version=program["current_version"],
            available_version = program.get("available_version") or None
        )

        programModel.save()