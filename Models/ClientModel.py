from typing import List, Optional

from Models.Model import Model


class ClientModel(Model):
    table_name = "clients"

    mac_address: str
    nickname: Optional[str]
    shutdown: bool
    installed_programs: Optional[List[str]]
    updatable_programs: Optional[List[str]]

    unique_field = "mac_address"

    def getMacAddress(self) -> str:
        return self.mac_address
    def setMacAddress(self, mac_address: str) -> None:
        self.mac_address = mac_address

    def getNickname(self) -> Optional[str]:
        return self.nickname
    def setNickname(self, nickname: str) -> None:
        self.nickname = nickname

    def getShutdown(self) -> bool:
        return self.shutdown
    def setShutdown(self, shutdown: bool) -> None:
        self.shutdown = shutdown


