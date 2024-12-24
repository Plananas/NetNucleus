import uuid
import ast

from Backend.App.Models.ClientModel import ClientModel
from Backend.App.Models.MessageController import MessageController
from Backend.App.Models.ProgramModel import ProgramModel
from Backend.App.Repositories.ClientRepository import ClientRepository


class ClientHandler:

    SHUTDOWN_COMMAND = "shutdown"
    GET_UPGRADES_COMMAND = "upgrades"
    GET_ALL_SOFTWARE_COMMAND = "software"
    INSTALL_SOFTWARE_COMMAND = "install"

    def __init__(self, client):
        self.messageController: MessageController = client
        self.connectedStatus = False
        self.clientModel = self.initializeClientModel()

    def shutdown(self):
        self.messageController.write(self.SHUTDOWN_COMMAND)

        #the client is shutting down so I think putting some kind of behaviour to check the status would be good
        response = self.messageController.read()
        return response

    def getUpdate(self):
        """
        :return: Array of Software available to update
        """
        self.messageController.write(self.GET_UPGRADES_COMMAND)

        responseArray = self.messageController.read()

        for response in responseArray:
            print(response)

        return responseArray

    def getAllSoftware(self):
        """
        :return: Array of Software
        """
        self.messageController.write(self.GET_ALL_SOFTWARE_COMMAND)

        responseArray = self.messageController.read()
        print("RESPONSE ARRAY")
        print(responseArray)
        responseArray = ast.literal_eval(responseArray)
        for response in responseArray:
            print(response)

        return responseArray

    def installSoftware(self, softwareName):
        """
        :return: Success Message
        """
        self.messageController.write((self.INSTALL_SOFTWARE_COMMAND + " " + softwareName))

        responseArray = self.messageController.read()
        print("RESPONSE ARRAY")
        print(responseArray)
        responseArray = ast.literal_eval(responseArray)
        for response in responseArray:
            print(response)

        return responseArray

    def initializeClientModel(self) -> ClientModel:
        macAndSoftware = self.getAllSoftware()
        macAddress = next(iter(macAndSoftware))

        clientRepository = ClientRepository()
        existingClient = clientRepository.get_client_by_mac_address(macAddress)

        if not existingClient:
            client_uuid = str(uuid.uuid4())
            print('Client does not exist: Creating Model')

            self.clientModel: ClientModel = ClientModel(
                    uuid = client_uuid,
                    mac_address = macAddress,
                    nickname = '',
                    shutdown = False,
                    updatable_programs = ''
                )
            self.clientModel.save()
            self.initializePrograms(client_uuid ,macAndSoftware[macAddress])
            return self.clientModel

        print('client exists')
        existingClient[0].setShutdown(False)
        return existingClient[0]

    def initializePrograms(self, client_uuid, installed_software):
        for program in installed_software:
            programModel = ProgramModel(
                client_uuid = client_uuid,
                program_id = program["id"],
                name = program["name"],
                version = program["version"],
            )
            programModel.save()