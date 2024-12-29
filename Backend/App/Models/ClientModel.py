from typing import List, Optional

from Backend.App.Models.Model import Model
from Backend.App.Models.ProgramModel import ProgramModel
from Backend.App.Repositories.ProgramRepository import ProgramRepository


class ClientModel(Model):
    table_name = "clients"

    uuid: str
    mac_address: str
    nickname: Optional[str]
    shutdown: bool
    updatable_programs: Optional[List[str]]

    unique_field = ""

    def get_uuid(self):
        return self.uuid

    def get_mac_address(self) -> str:
        return self.mac_address
    def set_mac_address(self, mac_address: str) -> None:
        self.mac_address = mac_address

    def get_nickname(self) -> Optional[str]:
        return self.nickname
    def set_nickname(self, nickname: str) -> None:
        self.nickname = nickname

    def get_shutdown(self) -> bool:
        return self.shutdown
    def set_shutdown(self, shutdown: bool) -> None:
        self.shutdown = shutdown

    def get_installed_programs(self) -> Optional[List[ProgramModel]]:
        program_repository = ProgramRepository()
        installed_programs = program_repository.get_program_by_client_id(self.uuid)

        return installed_programs
    @staticmethod
    def set_installed_programs(self, installed_programs: List[ProgramModel]) -> None:
        [program.save() for program in installed_programs]

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary for JSON serialization.
        """
        return {
            "uuid": self.uuid,
            "mac_address": self.mac_address,
            "nickname": self.nickname,
            "shutdown": self.shutdown,
            "updatable_programs": self.updatable_programs,
        }