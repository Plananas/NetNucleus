from Models.Message import Message


class ClientHandler:

    SHUTDOWN_COMMAND = "shutdown"
    GET_UPGRADES_COMMAND = "upgrades"
    GET_ALL_SOFTWARE_COMMAND = "software"

    def __init__(self, client):
        self.client: Message = client
        self.connectedStatus = False

    def shutdown(self):
        self.client.write(self.SHUTDOWN_COMMAND)

        #the client is shutting down so I think putting some kind of behaviour to check the status would be good
        response = self.read()
        return response

    def getUpdate(self):
        """
        :return: Array of Software available to update
        """
        self.client.write(self.GET_UPGRADES_COMMAND )

        responseArray = self.read()

        for response in responseArray:
            print(response)

        return responseArray

    def getAllSoftware(self):
        """
        :return: Array of Software
        """
        self.client.write(self.GET_ALL_SOFTWARE_COMMAND )

        responseArray = self.read()

        for response in responseArray:
            print(response)

        return responseArray

    def read(self):
        return {self.client.getMacAddress(): self.client.read()}