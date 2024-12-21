from Models.ClientModel import ClientModel
from Models.MessageController import MessageController
from Repositories.ClientRepository import ClientRepository


class ClientHandler:

    SHUTDOWN_COMMAND = "shutdown"
    GET_UPGRADES_COMMAND = "upgrades"
    GET_ALL_SOFTWARE_COMMAND = "software"

    def __init__(self, client):
        self.messageController: MessageController = client
        self.connectedStatus = False
        self.clientModel = self.initializeClientModel()

    def shutdown(self):
        self.messageController.write(self.SHUTDOWN_COMMAND)

        #the client is shutting down so I think putting some kind of behaviour to check the status would be good
        response = self.read()
        return response

    def getUpdate(self):
        """
        :return: Array of Software available to update
        """
        self.messageController.write(self.GET_UPGRADES_COMMAND)

        responseArray = self.read()

        for response in responseArray:
            print(response)

        return responseArray

    def getAllSoftware(self):
        """
        :return: Array of Software
        """
        self.messageController.write(self.GET_ALL_SOFTWARE_COMMAND)

        responseArray = self.read()

        for response in responseArray:
            print(response)

        return responseArray

    def read(self):
        return {self.messageController.getMacAddress(): self.messageController.read()}

    def initializeClientModel(self) -> ClientModel:
        macAndSoftware = self.getAllSoftware()
        macAddress = next(iter(macAndSoftware))

        clientRepository = ClientRepository()
        existingClient = clientRepository.get_client_by_mac_address(macAddress)

        if not existingClient:
            print('Client does not exist: Creating Model')
            self.clientModel: ClientModel = ClientModel(
                    mac_address = macAddress,
                    nickname = '',
                    shutdown = False,
                    installed_programs = macAndSoftware[macAddress],
                    updatable_programs = ''
                )

            return self.clientModel.save()

        print('client exists')
        return existingClient